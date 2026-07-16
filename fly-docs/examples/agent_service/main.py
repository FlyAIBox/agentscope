# -*- coding: utf-8 -*-
"""AgentScope Agent Service 启动示例脚本。

本脚本演示如何搭建并启动一个基于 FastAPI 的多租户、多会话 Agent 服务。
服务依赖 Redis 作为持久化存储，并可选接入 MCP 工具（浏览器自动化、高德地图等）。

运行前请确保：
    1. Python ≥ 3.11，且已安装 agentscope[full]
    2. Redis 已在 localhost:6379 运行
    3. Node.js ≥ 20（browser-use MCP 需要 npx）
    4. [可选] 设置环境变量 AMAP_API_KEY 以启用高德地图 MCP

启动方式：
    python main.py

服务默认监听 http://0.0.0.0:8000，可配合 examples/web_ui 中的 Web UI 使用。

详细文档：https://docs.agentscope.io/latest/en/deploy/agent-service
"""

import asyncio
import json
import os
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin
from urllib.request import Request, urlopen

import uvicorn
from fastapi import HTTPException, status
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from agentscope.app import create_app, SubAgentTemplate
from agentscope.app.message_bus import InMemoryMessageBus
from agentscope.app.rag.knowledge_base_manager import CollectionPerKbManager
from agentscope.app.storage import RedisStorage
from agentscope.app.workspace_manager import LocalWorkspaceManager
from agentscope.mcp import MCPClient, StdioMCPConfig, HttpMCPConfig
from agentscope.permission import PermissionContext, PermissionMode
from agentscope.rag import QdrantStore

DATA_DIR = os.getenv(
    "AGENTSCOPE_EXAMPLE_DATA_DIR",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), ".data"),
)
os.makedirs(DATA_DIR, exist_ok=True)


class CredentialProbeRequest(BaseModel):
    """用于从前端临时测试凭证，不会写入存储。"""

    data: dict[str, Any] = Field(description="Credential payload.")


class CredentialProbeResponse(BaseModel):
    """凭证测试与动态模型探测结果。"""

    ok: bool
    models: list[dict[str, Any]]
    total: int
    message: str


_DEFAULT_OPENAI_COMPATIBLE_BASE_URLS = {
    "openai_credential": "https://api.openai.com/v1",
    "dashscope_credential": "https://dashscope.aliyuncs.com/compatible-mode/v1",
    "deepseek_credential": "https://api.deepseek.com",
    "moonshot_credential": "https://api.moonshot.cn/v1",
}


def _field_to_str(value: Any) -> str | None:
    """把前端表单值或 Pydantic SecretStr 序列化后的值转成普通字符串。"""
    if value is None:
        return None
    if hasattr(value, "get_secret_value"):
        return value.get_secret_value()
    text = str(value).strip()
    return text or None


def _join_endpoint(base_url: str, endpoint: str) -> str:
    """Join URL paths without dropping nested gateway prefixes."""
    if base_url.rstrip("/").endswith(f"/{endpoint}"):
        return base_url.rstrip("/")
    return urljoin(f"{base_url.rstrip('/')}/", endpoint)


def _resolve_base_url(data: dict[str, Any]) -> str | None:
    credential_type = _field_to_str(data.get("type"))
    if credential_type == "ollama_credential":
        return _field_to_str(data.get("host")) or "http://localhost:11434"
    if credential_type == "xai_credential":
        host = _field_to_str(data.get("api_host")) or "api.x.ai"
        return (
            host
            if host.startswith(("http://", "https://"))
            else f"https://{host}/v1"
        )
    return _field_to_str(
        data.get("base_url"),
    ) or _DEFAULT_OPENAI_COMPATIBLE_BASE_URLS.get(credential_type or "")


def _request_json(url: str, headers: dict[str, str]) -> dict[str, Any]:
    request = Request(url, headers=headers, method="GET")
    try:
        with urlopen(request, timeout=15) as response:
            raw = response.read().decode("utf-8")
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace") or exc.reason
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"模型接口返回 {exc.code}: {detail}",
        ) from exc
    except URLError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"无法连接模型接口: {exc.reason}",
        ) from exc

    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="模型接口返回的不是有效 JSON。",
        ) from exc


def _looks_like_chat_model(model_name: str) -> bool:
    lowered = model_name.lower()
    non_chat_markers = (
        "embedding",
        "embed",
        "rerank",
        "moderation",
        "whisper",
        "tts",
        "dall-e",
        "bge-",
    )
    return not any(marker in lowered for marker in non_chat_markers)


def _guess_context_size(model_name: str) -> int:
    lowered = model_name.lower()
    if any(
        marker in lowered
        for marker in ("gpt-4.1", "gpt-5", "gemini-1.5", "gemini-2")
    ):
        return 1_048_576
    if "o4-mini" in lowered:
        return 200_000
    if any(
        marker in lowered
        for marker in ("gpt-4o", "deepseek", "moonshot", "kimi")
    ):
        return 128_000
    if "qwen" in lowered:
        return 131_072
    return 128_000


def _guess_output_size(model_name: str) -> int:
    lowered = model_name.lower()
    if any(marker in lowered for marker in ("gpt-4.1", "gpt-5", "o4-mini")):
        return 32_768
    if any(
        marker in lowered
        for marker in ("gpt-4o", "deepseek", "moonshot", "kimi", "qwen")
    ):
        return 16_384
    return 4_096


def _model_card(model_name: str) -> dict[str, Any]:
    lowered = model_name.lower()
    input_types = ["text/plain"]
    output_types = ["text/plain"]
    if any(
        marker in lowered
        for marker in ("vision", "4o", "4.1", "o4", "gpt-5", "vl")
    ):
        input_types.append("image/*")
    if "audio" in lowered:
        input_types.append("audio/*")
        output_types.append("audio/*")

    return {
        "type": "chat_model",
        "name": model_name,
        "label": model_name,
        "status": "active",
        "deprecated_at": None,
        "input_types": input_types,
        "output_types": output_types,
        "context_size": _guess_context_size(model_name),
        "output_size": _guess_output_size(model_name),
        "parameter_schema": {
            "type": "object",
            "properties": {},
            "required": [],
        },
        "parameters_overrides": {},
    }


def _extract_model_names(
    payload: dict[str, Any],
    credential_type: str | None,
) -> list[str]:
    if credential_type == "ollama_credential":
        items = payload.get("models", [])
        return [
            item["name"]
            for item in items
            if isinstance(item, dict) and isinstance(item.get("name"), str)
        ]

    items = payload.get("data", [])
    names = []
    for item in items:
        if isinstance(item, dict):
            value = item.get("id") or item.get("name")
            if isinstance(value, str):
                names.append(value)
        elif isinstance(item, str):
            names.append(item)
    return names


def _fetch_dynamic_models(data: dict[str, Any]) -> list[dict[str, Any]]:
    credential_type = _field_to_str(data.get("type"))
    base_url = _resolve_base_url(data)
    if not base_url:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="请先填写模型服务地址。",
        )

    headers: dict[str, str] = {"Accept": "application/json"}
    api_key = _field_to_str(data.get("api_key"))
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    organization = _field_to_str(data.get("organization"))
    if organization:
        headers["OpenAI-Organization"] = organization

    url = (
        _join_endpoint(base_url, "api/tags")
        if credential_type == "ollama_credential"
        else _join_endpoint(base_url, "models")
    )
    payload = _request_json(url, headers=headers)
    names = _extract_model_names(payload, credential_type)
    return [
        _model_card(name) for name in names if _looks_like_chat_model(name)
    ]


# ---------------------------------------------------------------------------
# 默认 MCP 工具配置
# MCP（Model Context Protocol）为 Agent 提供外部能力（浏览器、地图 API 等）。
# 此处定义的 MCP 会作为 workspace 的默认工具集，每个会话/workspace 自动继承。
# ---------------------------------------------------------------------------

default_mcps = [
    # browser-use：基于 Playwright 的浏览器自动化 MCP。
    # 通过 npx 动态拉取 @playwright/mcp，Agent 可打开网页、点击、填表等。
    # is_stateful=True 表示 MCP 会话在多次工具调用间保持浏览器状态（如已打开的页面）。
    MCPClient(
        name="browser-use",
        mcp_config=StdioMCPConfig(
            command="npx",
            args=["@playwright/mcp@latest"],
        ),
        is_stateful=True,
    ),
]

# 若设置了高德地图 API Key，则动态追加 amap MCP。
# 用于路线规划、POI 搜索等地理信息相关任务；无 Key 时不加载，避免启动失败。
if os.getenv("AMAP_API_KEY"):
    default_mcps.append(
        MCPClient(
            name="amap",
            mcp_config=HttpMCPConfig(
                url=f"https://mcp.amap.com/mcp?key="
                f"{os.environ['AMAP_API_KEY']}",
            ),
            # HTTP 型 MCP 无跨调用状态，每次调用独立。
            is_stateful=False,
        ),
    )

# ---------------------------------------------------------------------------
# 存储与向量库
# ---------------------------------------------------------------------------

# Redis 存储：会话、消息、凭证、知识库元数据等持久化均写入 Redis。
# 生产环境请确保 Redis 高可用；本地开发可用 brew/docker 启动单实例。
storage = RedisStorage(
    host="localhost",
    port=6379,
)

# 向量存储：知识库 RAG 检索的 embedding 存放处。
# 默认写入本地目录，避免重启后知识库向量索引丢失。
# 生产环境可改为持久化 Qdrant 服务（如 http://localhost:6333）。
vector_store = QdrantStore(location=os.path.join(DATA_DIR, "qdrant"))

# ---------------------------------------------------------------------------
# 创建 FastAPI 应用
# create_app 是 AgentScope 服务的主入口，自动注册会话、聊天、工作区、
# 知识库、定时任务等 HTTP 路由，并在 lifespan 中管理各组件生命周期。
# ---------------------------------------------------------------------------

app = create_app(
    # 持久化后端：见上方 RedisStorage 说明。
    storage=storage,
    # 消息总线：负责跨会话收件箱投递、空闲会话触发等实时消息。
    # InMemoryMessageBus 仅存在于单进程内存，多 worker / 多实例部署时消息无法互通。
    message_bus=InMemoryMessageBus(),
    # 若需多进程或生产部署，建议改用 Redis 消息总线（取消下方注释并替换上面的 InMemoryMessageBus）：
    #
    # from agentscope.app.message_bus import RedisMessageBus
    # message_bus=RedisMessageBus(
    #     host="localhost",
    #     port=6379,
    # ),
    # 工作区管理器：每个会话对应一个本地目录，Agent 在该目录内读写文件、执行命令。
    # basedir 下会为每个 workspace 创建子目录；default_mcps 注入默认 MCP 工具。
    workspace_manager=LocalWorkspaceManager(
        basedir=os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "workspaces",
        ),
        default_mcps=default_mcps,
    ),
    # 知识库管理器：启用 /knowledge-base 相关 API 与 Agent 侧 RAG 能力。
    # CollectionPerKbManager 为每个知识库分配独立 Qdrant collection，
    # 因此不同知识库可使用不同 embedding 维度，互不冲突。
    knowledge_base_manager=CollectionPerKbManager(
        storage=storage,
        vector_store=vector_store,
    ),
    # 自定义子 Agent 模板：团队模式下 Leader 可 spawn 指定类型的子 Agent。
    # 此处注册 "explorer" 类型——只读探索 Agent，用于读代码/文件但不修改。
    custom_subagent_templates=[
        SubAgentTemplate(
            type="explorer",
            # 类型描述会展示给 Leader Agent，用于决定何时委派探索任务。
            description=(
                "Read-only agents specialized in exploration tasks. It can "
                "read files but cannot modify, create, or delete them. Use "
                "this agent type when you need to investigate the codebase, "
                "understand its structure, or gather information from files "
                "to support planning—without making any changes."
            ),
            # 系统提示模板：{member_name}、{team_name}、{leader_name} 等占位符
            # 在 spawn 时由框架填充，形成该子 Agent 的角色与汇报规范。
            # 中文译文（下方 system_prompt_template 为运行时实际使用的英文原文）：
            #
            # 你是 {member_name}，团队「{team_name}」中的探索 Agent，由 {leader_name} 领导。
            #
            # 团队目标：{team_description}
            #
            # 你的角色：{member_description}
            #
            # ## 职责
            # - 完成团队 Leader 分配的探索任务。
            # - 你是只读的：可以查看文件和代码库，但绝不能修改、创建或删除任何内容。
            #
            # ## 汇报
            # - 无论任务成功或失败，都必须通过 TeamSay 工具向 {leader_name} 汇报任务结果。
            # - 私有推理过程保持私密；只分享 Leader 需要的结论与发现。
            #
            # 注意：`TeamSay` 是你与 {leader_name} 及其他团队成员沟通的唯一渠道。
            # 你产生的任何其他输出对他们不可见，因此你想让他们看到的任何内容都必须通过 `TeamSay` 发送。
            system_prompt_template="""You are {member_name}, an explorer \
agent in team '{team_name}' led by {leader_name}.

Team purpose: {team_description}

Your role: {member_description}

## Responsibilities
- Complete the exploration tasks assigned by the team leader.
- You are read-only: you may inspect files and the codebase, but you must \
never modify, create, or delete anything.

## Reporting
- Always report the task result back to {leader_name} using the TeamSay \
tool, whether the task succeeds or fails.
- Keep your private reasoning private; only share conclusions and findings \
that the leader needs.

Note: `TeamSay` is your ONLY channel to communicate with {leader_name} and \
the other team members. Any other output you produce is invisible to them, \
so anything you want them to see MUST be sent through `TeamSay`.""",
            # 权限上下文：EXPLORE 模式仅允许读操作，禁止写/删/执行等危险能力。
            permission_context=PermissionContext(
                mode=PermissionMode.EXPLORE,
            ),
        ),
    ],
    # 额外中间件：此处启用 CORS，允许 Web UI（可能运行在不同端口）跨域访问 API。
    # allow_origins=["*"] 便于本地开发；生产环境应收紧为具体前端域名。
    extra_middlewares=[
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_methods=["*"],
            allow_headers=["*"],
        ),
    ],
)


@app.post(
    "/credential/test",
    response_model=CredentialProbeResponse,
    summary="Test a credential and fetch dynamic models",
)
async def test_credential(
    body: CredentialProbeRequest,
) -> CredentialProbeResponse:
    """使用前端输入的地址和 key 临时拉取模型列表，验证凭证是否可用。"""
    models = await asyncio.to_thread(_fetch_dynamic_models, body.data)
    return CredentialProbeResponse(
        ok=True,
        models=models,
        total=len(models),
        message=f"连接成功，获取到 {len(models)} 个模型。",
    )


@app.post(
    "/model/from-credential",
    response_model=CredentialProbeResponse,
    summary="Fetch dynamic models from a credential payload",
)
async def list_models_from_credential(
    body: CredentialProbeRequest,
) -> CredentialProbeResponse:
    """按已保存或临时凭证动态获取模型列表，而不是只返回内置静态模型卡。"""
    models = await asyncio.to_thread(_fetch_dynamic_models, body.data)
    return CredentialProbeResponse(
        ok=True,
        models=models,
        total=len(models),
        message=f"获取到 {len(models)} 个模型。",
    )


if __name__ == "__main__":
    # 使用 uvicorn 启动 ASGI 服务。
    # "main:app" 表示从当前模块加载名为 app 的 FastAPI 实例；
    # reload=True 在代码变更时自动重载，开发友好，生产环境应设为 False。
    uvicorn.run(
        "main:app",
        host="0.0.0.0",  # 监听所有网卡，便于局域网或容器内访问
        port=8000,
        reload=True,
    )
