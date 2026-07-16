# Agentic Memory 中间件

本示例演示 `AgenticMemoryMiddleware`：一种以人类可读 Markdown 文件为后端的长期记忆中间件。

无需向量数据库或嵌入模型。

## 演示内容

`main.py` 在同一个工作区目录上，用单个 Agent 跑两轮对话：

1. **第 1 轮 — 持久化**
   - 接收包含可长期保存用户信息的模拟输入。
   - 被明确要求记住这些信息。
   - 使用内置 `Read` / `Write` 工具，在 `demo_workspace/Memory` 下创建或更新文件。

2. **第 2 轮 — 召回**
   - 同一 Agent 实例被问及先前的用户信息。
   - 根据中间件已落盘的 Markdown 记忆文件作答。

第一轮结束后，脚本会打印生成的 Markdown 文件，便于查看具体持久化了什么。

## 快速开始

按以下命令安装依赖：

```bash
git clone -b main https://github.com/agentscope-ai/agentscope

uv pip install agentscope
# 或从源码安装
# uv pip install -e .
```

运行示例：

```bash
cd agentscope/examples/long_term_memory/agentic_memory
export DASHSCOPE_API_KEY=sk-...; python main.py
```

演示工作区位于：

```text
examples/long_term_memory/agentic_memory/demo_workspace/
```

## Markdown 布局

中间件会自动创建如下目录：

```text
<workdir>/Memory/
`-- MEMORY.md
```

Agent 应将每条可长期保存的记忆写入带 frontmatter 的独立 Markdown 文件，并在 `MEMORY.md` 中添加简短指针：

```markdown
---
name: User profile
description: User lives in Hangzhou and prefers concise Chinese answers
type: user
---

Alice Chen lives in Hangzhou and prefers concise Chinese answers.
```

`MEMORY.md` 是索引，不是记忆正文：

```markdown
- [User profile](user_profile.md) — User location and answer-style preference.
```

后续轮次中，`MEMORY.md` 总会注入系统提示。中间件再根据文件名与 frontmatter 描述选出相关主题文件，并将其内容作为 hint 注入。

## 说明

- 记忆按工作区隔离：复用同一 `workdir` 即可复用同一套 Markdown 记忆。
- 新的 Agent 实例仍可召回先前事实，因为记忆存在磁盘上，而非 `Agent.state`。
- 当用户要求记住某事时，由 Agent 自行决定保存什么。
- `MEMORY.md` 应保持精简，因为它会进入每一次系统提示。
- 主题文件就是普通 Markdown，可用常规文件系统工具查看、编辑、提交、复制或删除。
