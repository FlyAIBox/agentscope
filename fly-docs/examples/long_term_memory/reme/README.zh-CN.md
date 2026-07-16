# ReMe 中间件示例

一份可运行的演示（`reme_demo.py`），展示如何将
[ReMe](https://github.com/agentscope-ai/ReMe) 中间件接入
`agentscope.agent.Agent`。连续驱动两轮共享同一 ReMe 工作区的 agent
**会话**，从而可见 ReMe 的跨会话记忆效果；并内联打印每次中间件贡献
（检索 / 工具调用 / 回写），便于观察各路径何时触发。

ReMe 是 AgentScope 团队自研的基于文件的记忆工具包。与 mem0 不同，它
**嵌入进程内运行**——无需单独启动服务——并通过**监听对话**记录记忆：
每次回复后，新的对话交换经 ReMe 的 `auto_memory` 任务自动回写。
agent 从不自行保存记忆；也没有 add 工具。演示用 AgentScope 自带的
DashScope 对话模型（驱动 LLM 支持的 `auto_memory` 回写）与 DashScope
嵌入模型（向量检索）驱动 ReMe，二者均注入到嵌入式应用中。

ReMe 自带的 `default` 配置仅用 **BM25（关键词）** 搜索——其文件存储
默认关闭向量库。长期*记忆*演示需要**语义**召回（「画月度销售图」应能
找到「偏好 matplotlib」卡片），因此 `reme_demo.py` 会注入
`embedding_model`——这会自动开启 ReMe 向量库；详见下文。

## 安装

```bash
# reme-ai 是 AgentScope 的可选依赖——通过 extra 安装：
pip install "agentscope[reme]"
# （等价于 `pip install agentscope reme-ai`）

export DASHSCOPE_API_KEY=sk-...
```

## 导入路径

`ReMeMiddleware` 从 middleware 包导出：

```python
from agentscope.middleware import ReMeMiddleware
from agentscope.tool import Toolkit
```

## 构造

中间件会构建并**拥有**一个嵌入式 `reme.ReMe` 应用——在首次使用时惰性创建，
并由 `await mw.close()` 拆除。用普通参数配置即可，无需管理外部应用。
用户可调设置位于嵌套的 `Parameters` 模型上（agent 服务会将其 JSON schema
渲染为表单）：

```python
ReMeMiddleware(
    workspace_dir=".reme",
    parameters=ReMeMiddleware.Parameters(
        chat_model=my_chat_model,        # 注入到 ReMe 的 LLM 组件，
                                         #   驱动 auto_memory 回写
        embedding_model=my_embedding_model,  # 注入到嵌入组件；
                                             #   同时自动开启 ReMe 向量库
        mode="both",
        top_k=5,
    ),
)
```

两个模型在应用生命周期内固定（从不取自某个 agent），因此即便一个中间件
实例被多个 agent 共享，嵌入式应用的单一 LLM / 嵌入组件也定义明确。

| `chat_model` / `embedding_model` | 行为 |
|:-:|---|
| 已提供 | 启动时注入到 ReMe 默认 LLM / 嵌入组件；只需 DashScope key。提供 `embedding_model` 还会开启向量库以支持语义搜索。 |
| 省略 | ReMe 使用自身配置/凭证中的 LLM / 嵌入后端；搜索保持仅关键词。 |

> **为何注入 `embedding_model`？** ReMe 在 `start()` 时会急切启动嵌入组件——
> 即便是 BM25-only 默认配置——并根据配置中的凭证构建。注入 AgentScope
> `embedding_model` 可绕过该凭证路径，因此你只需 DashScope key。这也是
> 向量搜索的动力：提供它会自动将 ReMe 文件存储从仅 BM25 切换为向量库。

## 中间件如何控制记忆

无论何种模式，ReMe **总会**在每次回复后通过 `auto_memory` 回写新对话——
`mode` 只决定 agent **如何检索**：

### `static_control`
中间件完成检索，agent 无感知：

1. **`on_reply`（pre）** 启动后台 `asyncio` 任务，用最新用户消息搜索
   ReMe，与回复并发执行。
2. **`on_reasoning`** 在每步推理前轮询该任务；完成后，中间件向
   `state.context` 追加一条 `AssistantMsg(name="memory", ...)` 的
   `HintBlock`，使*下一次*模型调用能看到它。注入是**尽力而为**：
   单次回复（一次模型调用）可能在检索完成前结束，因此 hint 可能落在
   后续步骤，或本轮被跳过——与 `AgenticMemoryMiddleware` 的权衡相同。
   含工具调用的轮次（两步及以上推理）注入更可靠。
3. **`on_reply`（post）** 经 `auto_memory` 回写新的 `(user, assistant)` 对话。

注入的记忆消息会**持久留在** agent 的 context 中跨轮累积。若长会话积累过多，
可用 `compress_context` 或自定义中间件后处理。

### `agent_control`
中间件暴露单个 `memory_search(query, limit)` 工具，除此之外不加干预
（自动回写仍会运行）。构造 agent 时需显式传入 toolkit：

```python
mw = ReMeMiddleware(..., mode="agent_control")
agent = Agent(
    ...,
    toolkit=Toolkit(tools=await mw.list_tools()),
    middlewares=[mw],
)
```

系统提示会有简短提示，告知 agent 存在搜索工具；各工具用法通过标准
tool schema 提供。无自动检索。

### `both`（默认）
两条检索路径同时生效：记忆会自动检索并以 assistant 备注形式追加到
agent context，同时暴露 `memory_search` 工具（含系统提示 hint）供显式
按需搜索。

## 记忆作用域（`session_id`）

ReMe 按 **`session_id`** 划分回写作用域，在 hook 时从
`agent.state.session_id` 实时读取——从不存在中间件上。搜索则是
**工作区范围**（跨所有会话），因此后续会话即使 `session_id` 不同，
也能召回先前会话的记忆。若要固定可恢复的会话，在 agent 上设置 id：

```python
from agentscope.state import AgentState

agent = Agent(..., state=AgentState(session_id="alice-main"))
```

演示正是这样做的——`session-1` 写入偏好，`session-2`（全新 agent、
空聊天 context）通过共享工作区召回。

## 跨 agent 共享一个中间件

由于 `session_id` 按次读取（不存储），且对话模型在构造时固定
（绑定到嵌入式应用的单一 LLM），**一个** `ReMeMiddleware` 可安全地
被多个 agent 与会话共享——构建一次并传给每个 agent：

```python
mw = ReMeMiddleware(
    workspace_dir=".reme",
    chat_model=chat_model,
    embedding_model=embedding_model,
    mode="both",
)
agent_a = Agent(..., middlewares=[mw], state=AgentState(session_id="a"))
agent_b = Agent(..., middlewares=[mw], state=AgentState(session_id="b"))
```

演示即采用此做法。关闭时调用 `await mw.close()` 拆除嵌入式应用
（AgentScope 不管理中间件生命周期）。

## 配置

`config` 选择一份 ReMe 配置（默认捆绑的 `"default"`，即自动记忆 +
**仅 BM25** 搜索——其文件存储自带 `embedding_store: ""`）。要启用
**向量搜索**，请提供 `embedding_model`（演示即如此）——中间件会自动将
ReMe 文件存储接到默认 embedding store：

```python
ReMeMiddleware(
    workspace_dir=".reme",
    parameters=ReMeMiddleware.Parameters(
        embedding_model=my_embedding_model,  # 开启向量库
    ),
)
```

否则 ReMe 的 `as_llm` / `as_embedding` 组件由其自身配置中的环境变量
（`LLM_API_KEY`、`EMBEDDING_API_KEY` 等）驱动；注入 AgentScope
`chat_model` / `embedding_model` 可绕过它们。若需要专用参数未覆盖的配置，
可将 `config` 指向你自己的 ReMe 配置文件。完整组件集见 ReMe 的
`default.yaml`。

> **说明（索引）：** `auto_memory` 回写在日卡写入磁盘后即返回；卡片需经
> ReMe 索引后才可被搜索。演示在每次写入后强制同步 `reindex`，使下一次
> 读取确定性可见，而不依赖 ReMe 的后台索引循环。见 `reme_demo.py` 中的
> `_reindex`。
