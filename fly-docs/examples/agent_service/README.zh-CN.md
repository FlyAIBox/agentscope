# Agent Service（Agent 服务）

> [English](README.md)

Agent Service 是基于 FastAPI 构建的多租户、多会话服务，使用 AgentScope 2.0 实现。

本示例演示：

- 如何配置基于 Redis 存储的 Agent 服务
- 如何启动服务及其配套的 Web UI

关于 Agent Service 的更多细节，请参阅[官方教程](https://docs.agentscope.io/latest/en/deploy/agent-service)。

## 环境要求

- Python ≥ 3.11
- Node.js ≥ 20，且已安装 `npx`
- [可选] 环境变量 `AMAP_API_KEY` 中配置高德地图 API Key（用于 `amap` MCP）

## 快速开始

从 PyPI 或源码安装 AgentScope：

```bash
uv pip install agentscope[full]
# 或从源码安装
# uv pip install -e [full]
```

安装并启动 Redis 作为后端存储：

```bash
# macOS (Homebrew)
brew install redis
brew services start redis

# Linux (systemd)
sudo apt install redis-server
sudo systemctl start redis-server

# Docker（跨平台）
docker run --rm -p 6379:6379 redis:7
```

启动 Agent 服务：

```bash
cd examples/agent_service

python main.py
```

在另一个终端启动 Web UI，体验聊天式交互界面：

```bash
cd examples/web_ui/

pnpm install
# 或 npm install

# 开发模式运行
pnpm dev
```

启动后，在 Web UI 中将 API 地址设置为 `http://localhost:8000`，即可开始使用 Agent 服务。

<img src="https://gw.alicdn.com/imgextra/i2/O1CN01Phmg1G1brIVC8WXyU_!!6000000003518-2-tps-2938-1736.png" alt="Web UI 截图" width="100%">

## 下一步

- 可在 `main.py` 中自定义服务，例如添加 MCP 工具、中间件或自定义工作区管理器实现。

- 体验 Agent 服务的更多能力，包括：
    - 人机协同交互与权限系统
<img src="https://gw.alicdn.com/imgextra/i1/O1CN01vGGiBw20agWwpzmjy_!!6000000006866-2-tps-2934-1732.png" alt="权限系统" width="100%">

    - 定时任务
<img src="https://gw.alicdn.com/imgextra/i1/O1CN01Xi3Qw71E2haKKu4z0_!!6000000000294-2-tps-2932-1738.png" alt="定时任务" width="100%">

    - 更多功能，敬请期待后续更新
