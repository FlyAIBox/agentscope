# RAG 示例

两段以库模式演示 `agentscope.rag` 的脚本——不依赖 FastAPI 服务、manager 或消息总线。每个脚本手动组装解析器、分块器、嵌入模型、向量库与 `KnowledgeBase`，以便端到端看清数据流。

| 脚本 | 演示内容 |
| --- | --- |
| [`index_and_search.py`](./index_and_search.py) | 最小流水线：解析 → 分块 → 嵌入 → 写入，再调用 `KnowledgeBase.search`。建议从这里开始。 |
| [`integrate_with_agent.py`](./integrate_with_agent.py) | 通过 `RAGMiddleware` 将同一 `KnowledgeBase` 挂到 `Agent` 上，分别演示 `static`（自动注入）与 `agentic`（工具驱动）两种模式。 |

两个示例都使用内存版 Qdrant（`location=":memory:"`）和 DashScope `text-embedding-v4` 模型，因此无需额外外部服务。

## 安装

```bash
# 从 PyPI 安装
uv pip install "agentscope[rag]"

# 或从源码安装（仓库根目录）
uv pip install -e ".[rag]"
```

若想用本地持久化的 Milvus Lite 向量库替代内存版 Qdrant，需安装对应可选依赖：

```bash
uv pip install "agentscope[milvuslite]"
# 或从源码安装（仓库根目录）
uv pip install -e ".[milvuslite]"
```

然后将向量库构造替换为：

```python
from agentscope.rag import MilvusLiteStore

store = MilvusLiteStore(uri="./rag_demo.db")
```

`integrate_with_agent.py` 还会用到 `DashScopeChatModel`，该依赖已包含在基础 `agentscope` 包中。

## 运行

```bash
export DASHSCOPE_API_KEY=sk-...

python examples/rag/index_and_search.py
python examples/rag/integrate_with_agent.py
```

## 服务模式

上述两个脚本是库模式——在同一进程里自行驱动流水线。若需要完整的服务模式体验（知识库 CRUD、文档上传、索引 worker、检索等 FastAPI 接口），请参见后端示例 [`examples/agent_service`](../agent_service)，以及对话式 UI [`examples/web_ui`](../web_ui)。
