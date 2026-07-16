# mem0 中间件示例

一份可运行的演示（`oss_demo.py`），展示如何将
[mem0](https://github.com/mem0ai/mem0) 中间件接入
`agentscope.agent.Agent`。针对同一 `user_id` 连续驱动两轮 agent
会话，从而可见 mem0 的跨会话记忆效果；并内联打印每次中间件贡献
（检索 / 工具调用 / 回写），便于观察各路径何时触发。

演示默认使用 **OSS 后端**（开源 mem0，经本地 Qdrant 自托管），且
mem0 由 AgentScope 自带的 DashScope 对话与嵌入模型驱动——无需再为
mem0 单独准备 OpenAI key。若要改为对接托管的 **mem0 Platform**，
将 `Mem0Middleware(...)` 的构造方式换成脚本内标注的备选写法
（在 `oss_demo.py` 中搜索
``# For the hosted mem0 Platform, swap …`` 注释）即可——演示其余部分相同。

## 安装

```bash
# mem0 是 AgentScope 的可选依赖——通过 extra 安装：
pip install "agentscope[mem0]"      # 解析为 mem0ai>=2.0.0,<3.0.0
# （等价于 `pip install agentscope mem0ai>=2.0.0,<3.0.0`）

export DASHSCOPE_API_KEY=sk-...     # OSS 路径
# Platform 路径（仅在切换后需要）：
# export MEM0_API_KEY=m0-...
# export OPENAI_API_KEY=sk-...      # 仅当 agent 的对话模型是 OpenAI 时需要
```

## 导入路径

`Mem0Middleware` 从 middleware 包导出：

```python
from agentscope.middleware import Mem0Middleware
from agentscope.tool import Toolkit
```

## 三种构造路径

```python
# 1. Models — 用你的 AgentScope 对话 + 嵌入模型，构建本地 OSS AsyncMemory。
#    其余配置走 mem0 默认值。
Mem0Middleware(
    user_id="alice",
    chat_model=my_chat_model,
    embedding_model=my_embedding_model,
    mode="both",
)

# 2. Models + 自定义 mem0_config — 与 (1) 相同，但从你自定义的
#    MemoryConfig 起步（自定义向量库、历史 DB、reranker 等）。
#    `chat_model` / `embedding_model` 始终优先：
#    若 mem0_config 已指定 .llm 或 .embedder，会被由你的模型构建的
#    AgentScope adapter 覆盖。mem0_config 的其余字段（vector_store、
#    history_db_path、reranker 等）原样保留。
Mem0Middleware(
    user_id="alice",
    chat_model=my_chat_model,
    embedding_model=my_embedding_model,
    mem0_config=MemoryConfig(
        vector_store=VectorStoreConfig(
            provider="qdrant",
            config={"host": "my-qdrant", "port": 6333},
        ),
        history_db_path="/data/mem0_history.db",
    ),
    mode="both",
)

# 3. Client — 传入你已构建好的 mem0 client。接受任一后端：
#    `mem0.AsyncMemory`（开源 / 自托管）或
#    `mem0.AsyncMemoryClient`（托管 Platform）。适合需要完全控制
#    mem0 配置的场景——自定义子类、跨多个 agent 复用预热后的 client、
#    或无法用 `build_mem0_config` 表达的特殊配置等。
#
# OSS 后端（自行组装 AsyncMemory）：
Mem0Middleware(
    user_id="alice",
    client=AsyncMemory(),  # 或 AsyncMemory.from_config({...})
    mode="both",
)

# 托管 Platform 后端：
Mem0Middleware(
    user_id="alice",
    client=AsyncMemoryClient(api_key="m0-..."),
    mode="both",
)
```

优先级与校验矩阵：

| `client` | `mem0_config` | `chat_model` | `embedding_model` | 行为 |
|:-:|:-:|:-:|:-:|---|
| ✓ | — | — | — | 原样使用 `client`。 |
| ✓ | 任意 | 任意 | 任意 | 使用 `client`；其余三个参数被忽略，并打 `WARNING` 日志列出被丢弃的 kwargs。 |
| — | ✓ | — | — | 用 `mem0_config` 包装为 `AsyncMemory`，不做覆盖。 |
| — | ✓ | ✓ | — | 包装并覆盖 `.llm`（AgentScope adapter）；保留 `mem0_config` 中的 `.embedder`。 |
| — | ✓ | — | ✓ | 包装并仅覆盖 `.embedder`；保留 `mem0_config` 中的 `.llm`。 |
| — | ✓ | ✓ | ✓ | 包装并同时覆盖 `.llm` 与 `.embedder`（`mem0_config` 其余字段保留）。 |
| — | — | ✓ | ✓ | 新建 `MemoryConfig`（向量库 / 历史 DB 用 mem0 默认），并接入 AgentScope adapter。 |
| — | — | ✓ | — | ❌ `ValueError` — 省略 `mem0_config` 时，`chat_model` 与 `embedding_model` 必须成对传入。 |
| — | — | — | ✓ | ❌ 同上。 |
| — | — | — | — | ❌ `ValueError` — 需要其一：`client`、`mem0_config`，或同时提供 `chat_model` + `embedding_model`。 |

为何存在「client 优先」与「config 覆盖」路径：

- **`client` 优先** 让同一种 `Mem0Middleware(...)` 调用形态，同时服务库模式调用方（传入 AgentScope 模型）与生产环境（提供预构建 `client`）。`WARNING` 日志能暴露不匹配，而不直接崩溃。
- **对 `mem0_config.llm` / `.embedder` 的覆盖** 让你可以维护一份规范的 `MemoryConfig` 模板（自定义向量库、历史 DB、reranker 等），再在各调用点通过传入 `chat_model` / `embedding_model` 只替换 LLM / embedder。

## 中间件如何控制记忆

`mode` 参数在三种模式中选择。差异在于 **LLM 看到什么** 以及 **哪些步骤会自动触发**：

### `static_control`
中间件完成工作，agent 无感知。对齐 AgentScope 1.x 的
`ReActAgent._retrieve_from_long_term_memory`：

1. **`on_reply`（pre）** 用最新用户消息查询 mem0，并预取结果。
2. **在 `ReplyStartEvent` 时**——该事件在 agent 将新用户输入写入
   `state.context` 之后、推理循环开始之前触发——中间件向
   `state.context` 追加一条 `AssistantMsg(name="memory", ...)`。
   这样记忆备注会紧挨在用户新消息之后，与 v1 的位置一致
   （v1 在 `self.memory.add(msg)` 之后立刻执行）。
3. **`on_reply`（post）** 将新的 `(user, assistant)` 对话回写到 mem0。

注入的记忆消息会**持久留在** agent 的 context 中跨轮累积。长会话里，
凡检索到内容的轮次都会多一条；若 token 成为问题，可用
`compress_context` 后处理，或自行编写中间件弹出它们。

### `agent_control`
中间件暴露两个工具——`search_memory(keywords, limit)` 与
`add_memory(thinking, content)`——除此之外不加干预。
构造 agent 时需显式传入 toolkit：

```python
mw = Mem0Middleware(..., mode="agent_control")
agent = Agent(
    ...,
    toolkit=Toolkit(tools=await mw.list_tools()),
    middlewares=[mw],
)
```

系统提示会有简短提示，告知 agent 存在记忆工具；各工具的具体用法
通过标准 tool schema 提供。无自动检索或回写。

### `both`（默认）
两种模式同时生效：记忆会自动检索并以 assistant 备注形式追加到
agent context，同时暴露工具（含系统提示 hint）供显式按需搜索 / 保存。
这与 AgentScope 1.x 的 `ReActAgent.long_term_memory_mode` 默认行为一致。

## 跨 agent 共享一个中间件

本地 OSS mem0 后端默认使用磁盘版 Qdrant，而 Qdrant 会对存储目录
（默认 ``/tmp/qdrant``）加**排他锁**。若用 `chat_model` +
`embedding_model` 各建一个 `Mem0Middleware`，会各自构造
`AsyncMemory`——第二个会因锁冲突崩溃：

```
RuntimeError: Storage folder /tmp/qdrant is already accessed by
another instance of Qdrant client.
```

修复方式：只构建 **一个** `Mem0Middleware` 实例，并传给所有应共享
同一记忆命名空间的 agent：

```python
mw = Mem0Middleware(
    user_id="alice",
    chat_model=chat_model,
    embedding_model=embedding_model,
    mode="both",
)
agent_a = Agent(
    ...,
    toolkit=Toolkit(tools=await mw.list_tools()),
    middlewares=[mw],
)
agent_b = Agent(
    ...,
    toolkit=Toolkit(tools=await mw.list_tools()),
    middlewares=[mw],
)
```

演示即采用此做法。记忆工具在调用时拿到实时 `AgentState`，中间件
通过 `state.session_id` 解析当前 agent，因此跨 agent 共享同一中间件是安全的。

若确实需要每个 agent 独立的 Qdrant 存储，可为每个实例传入不同
``vector_store.config.path`` 或 ``collection_name`` 的 ``mem0_config``。

### 推荐：用 Docker 运行 Qdrant（尤其在 Windows 上）

本地磁盘版 Qdrant 适合单进程演示，但在真实部署中较脆弱——在
**Windows 上尤其痛苦**：文件系统锁语义与 Unix 不同，排他锁失败也更难恢复。
超出单进程 Linux/macOS 沙箱的场景，请将 Qdrant 作为服务运行：

```bash
docker run -p 6333:6333 -p 6334:6334 \
    -v $(pwd)/qdrant_storage:/qdrant/storage \
    qdrant/qdrant
```

然后让 mem0 指向该服务，而非磁盘路径：

```python
from mem0.configs.base import MemoryConfig
from mem0.vector_stores.configs import VectorStoreConfig

mem0_cfg = MemoryConfig(
    vector_store=VectorStoreConfig(
        provider="qdrant",
        config={
            "collection_name": "mem0",
            "host": "localhost",     # Docker 容器
            "port": 6333,
            "embedding_model_dims": 1536,
        },
    ),
)
Mem0Middleware(
    user_id="alice",
    chat_model=chat_model,
    embedding_model=embedding_model,
    mem0_config=mem0_cfg,
)
```

相对磁盘版的好处：

- 无文件锁争用——多个 Python 进程可同时连接。
- 跨次运行可保留数据，无需手动清理文件。
- 同一形态也适用于远程 Qdrant（Qdrant Cloud、自建 Kubernetes）——
  只需改 ``host`` / ``port`` / ``api_key``。

## 记忆作用域（`user_id` × `agent_id`）

mem0 在 `add` 时用传入的 `user_id` 与 `agent_id` 过滤值给每条记忆打标签，
搜索时对这些标签做 AND 匹配。中间件通过 `scope_search_by_agent`
标志（默认 `True`）暴露 agent 维度：

| `scope_search_by_agent` | `add` 给记忆打的标签 | `search` 的过滤条件 | 效果 |
| --- | --- | --- | --- |
| `True`（默认） | `user_id` + `agent_id` | `user_id` + `agent_id` | 严格按 agent 隔离。同一用户下，agent A 的记忆对 agent B 不可见。 |
| `False` | `user_id` + `agent_id`（不变） | 仅 `user_id` | 读宽写窄。同一用户下所有 agent 共享记忆池，但每条记忆仍记录写入它的 agent（可见于 mem0 metadata）。 |

`agent_id` 默认为 `agent.name`。可在中间件构造时通过 `agent_id="..."`
或 `agent_id=lambda agent: ...` 覆盖。

何时放宽 `scope_search_by_agent`：

- 同一用户有多个专职 agent（研究 / 编码 / 日程），希望彼此关于用户的发现可互相受益。
- agent 的 `name` 可能在不同部署间变化，但仍希望记忆跨名称变更保留。

### 关于以 agent 为中心的抽取（当前不可达）

mem0 v2 的抽取提示
（[`ADDITIVE_EXTRACTION_PROMPT`](https://github.com/mem0ai/mem0/blob/main/mem0/configs/prompts.py)）
有一段条件后缀，会将表述从以用户为中心（「用户说了 X」）切换为
**以 agent 为中心**（「Agent 获知 X」/「Agent 推荐了 Y」）。触发条件是
`is_agent_scoped = bool(filters.agent_id) and not filters.user_id`——
即仅在提供了 `agent_id` *且未提供* `user_id` 时。中间件总会传入
`user_id`（构造必填），因此该 agent 中心后缀目前无法通过
`Mem0Middleware` 到达。实践中这通常没问题——agent 人设 / 配置一般通过
系统提示表达，而非长期记忆。

## 服务模式集成（`agentscope.app`）

上述演示使用**库模式**——自行构造 `Agent`，并将 `Mem0Middleware`
传入 `middlewares=[...]`。若通过 `agentscope.app`（FastAPI 服务层）
做生产部署，`user_id` 已由框架从 `X-User-ID` HTTP 头传入。可通过
[`extra_agent_middlewares`](../../../../src/agentscope/app/_types.py)
工厂接入：

```python
from agentscope.app import create_app
from agentscope.middleware import Mem0Middleware
from agentscope.middleware._longterm_memory._mem0._agentscope_adapter \
    import build_mem0_config
from mem0 import AsyncMemory

# 在模块作用域只构建一次 mem0 client——本地 OSS Qdrant
# 会对存储目录加排他锁；按请求构造会在并发流量下死锁。
chat_model = ...     # 共享的 AgentScope ChatModelBase
emb_model  = ...     # 共享的 AgentScope EmbeddingModelBase
mem0_client = AsyncMemory(
    config=build_mem0_config(
        chat_model=chat_model,
        embedding_model=emb_model,
    ),
)


async def long_term_memory_factory(
    user_id: str,         # ← 来自已认证的 X-User-ID 头
    agent_id: str,
    session_id: str,
) -> list:
    return [
        Mem0Middleware(
            user_id=user_id,
            client=mem0_client,    # 跨所有请求共享
            mode="both",
        ),
    ]


app = create_app(
    ...,
    extra_agent_middlewares=long_term_memory_factory,
)
```

要点：

- 工厂签名为 `async (user_id, agent_id, session_id) ->
  list[MiddlewareBase]`，在**每次组装 agent 时调用一次**
  （即每次聊天轮次 / 定时触发）。每次返回新的 `Mem0Middleware`
  实例，但共享同一个底层 mem0 client。
- `user_id` 是已认证调用方，由 `agentscope.app` 经
  `get_current_user_id` 注入（当前来自 `X-User-ID` 头；上游接入
  鉴权后将改为 JWT）。直接传给
  `Mem0Middleware(user_id=user_id, ...)` 即可——无需 resolver 可调用对象。
- 对接托管 mem0 Platform 时，将 `AsyncMemory(config=...)` 换成
  `AsyncMemoryClient(api_key=...)`——工厂形态相同，也无 Qdrant 锁问题。

## AgentScope 作为 mem0 后端路径的说明

传入 `chat_model` + `embedding_model` 时，中间件内部会：

1. 在 mem0 的工厂字典中，以 provider 名 `"agentscope"` 注册
   `AgentScopeLLM` / `AgentScopeEmbedding`。
2. 用允许 `"agentscope"` 的子类替换 `LlmConfig` / `EmbedderConfig`
   （mem0 原有 validator 硬编码了白名单，不含我们）。其他 provider
   仍按 mem0 原始错误被拒绝。
3. 构建 `AsyncMemory`，使其 `.llm` 与 `.embedding_model` 经
   AgentScope adapter 路由。
4. 通过持久后台事件循环，将 mem0 的同步 API 桥接到 AgentScope 的
   异步模型，使异步客户端（如 Ollama 的 `AsyncClient`）能跨调用
   保持连接池。

你的嵌入模型 `dimensions` 必须与向量库期望维度一致——mem0 默认
Qdrant 期望 1536，对应 DashScope `text-embedding-v2` 的
`dimensions=1536`（`oss_demo.py` 所用值）。
