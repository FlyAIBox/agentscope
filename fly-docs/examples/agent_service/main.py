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
import os

import uvicorn
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware

from agentscope.app import create_app, SubAgentTemplate
from agentscope.app.message_bus import InMemoryMessageBus
from agentscope.app.rag.knowledge_base_manager import CollectionPerKbManager
from agentscope.app.storage import RedisStorage
from agentscope.app.workspace_manager import LocalWorkspaceManager
from agentscope.mcp import MCPClient, StdioMCPConfig, HttpMCPConfig
from agentscope.permission import PermissionContext, PermissionMode
from agentscope.rag import QdrantStore

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
# location=":memory:" 表示进程内内存 Qdrant，重启后数据丢失，仅适合示例/开发。
# 生产环境应改为持久化 Qdrant 服务（如 http://localhost:6333）。
vector_store = QdrantStore(location=":memory:")

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
