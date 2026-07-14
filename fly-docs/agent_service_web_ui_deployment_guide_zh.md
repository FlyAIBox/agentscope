# AgentScope Agent Service 与 Web UI 安装部署手册

本文适用于本仓库中的以下示例：

- Agent Service：`fly-docs/examples/agent_service/`
- Web UI：`fly-docs/examples/web_ui/`

本文坚持使用 AgentScope 源码和项目根目录的 `.venv`，核心安装命令为：

```bash
source .venv/bin/activate
uv pip install -e .
```

文档中的命令已于 2026-07-12 在 Linux ARM64、Python 3.11.15、uv 0.11.28、Node.js 22.14.0、pnpm 11.12.0 环境中实际执行验证；macOS（Homebrew Node / 本机 Redis、无 Docker、无 Corepack）场景亦按本文补充步骤验证过启动脚本。

## 快速启动脚本

仓库已提供统一管理脚本：`fly-docs/start_agent_service_web_ui.sh`。

首次使用：

```bash
cd /root/code/agentscope
./fly-docs/start_agent_service_web_ui.sh install
./fly-docs/start_agent_service_web_ui.sh start
```

日常管理：

```bash
# 查看状态
./fly-docs/start_agent_service_web_ui.sh status

# 查看最近日志
./fly-docs/start_agent_service_web_ui.sh logs
./fly-docs/start_agent_service_web_ui.sh logs -n 50

# 持续查看指定服务日志（支持 -f / -n / --tail）
./fly-docs/start_agent_service_web_ui.sh logs -f agent-service
./fly-docs/start_agent_service_web_ui.sh logs --tail 200 -f web-frontend

# 重启或停止脚本管理的应用进程
./fly-docs/start_agent_service_web_ui.sh restart
./fly-docs/start_agent_service_web_ui.sh stop
```

脚本自动定位仓库、激活 `.venv`、检查运行依赖和端口，并依次启动 Redis、Agent Service、Web UI Backend 与 Web UI Frontend。行为要点：

- 复用端口上已经健康运行的服务。
- 无 Docker 但本机有 `redis-server` 时，自动以后台方式启动本机 Redis。
- 不依赖 Linux 专用的 `setsid`；macOS 等环境用 Python 创建独立会话并记录真实 PID。
- 后台启动 `pnpm` 时设置 `CI=true`，并在 `fly-docs/examples/web_ui/.npmrc` 中关闭 `confirm-modules-purge`，避免非 TTY 下重建 `node_modules` 失败。
- `stop` / `restart` 会停止脚本记录的应用进程；若 PID 文件丢失，仍会尝试回收 8000 / 3000 / 5173 上的残留监听进程。默认不停止 Redis。

## 1. 服务结构与端口

| 组件 | 默认端口 | 用途 | 是否必需 |
| --- | ---: | --- | --- |
| Redis | 6379 | Agent、会话、凭据和任务等数据存储 | 是 |
| Agent Service | 8000 | AgentScope FastAPI 服务 | 是 |
| Web UI 前端 | 5173 | Vite 开发服务器 | 本地开发时是 |
| Web UI 后端 | 3000 | 示例 Node.js 健康检查接口 | 使用 `pnpm dev` 时启动 |

Web UI 前端会把用户在初始化页面填写的 Agent Service 地址保存到浏览器 `localStorage`，并直接请求该地址。当前 Node.js 后端只提供 `/api/health`，不是 Agent Service 的反向代理。

## 2. 前置条件

- Python 3.11 或更高版本
- uv
- Node.js 20 或更高版本
- pnpm
- Docker，或者本机可用的 Redis 7

检查环境：

```bash
python3 --version
uv --version
node --version
pnpm --version
docker --version || true
redis-server --version || true
```

macOS 无 Docker 时，前置条件改为本机 Redis 即可：`brew install redis`。

若没有 pnpm，优先使用 Node.js 自带的 Corepack：

```bash
corepack enable
corepack prepare pnpm@11.12.0 --activate
pnpm --version
```

若出现 `command not found: corepack`（常见于 Homebrew 安装的 Node，其配方通常不附带 Corepack），改用 npm 全局安装同一版本：

```bash
npm install -g pnpm@11.12.0
pnpm --version
```

## 3. AgentScope 源码安装

进入仓库根目录。下文假设源码位于 `/root/code/agentscope`；其他机器请替换成实际绝对路径。

```bash
cd /root/code/agentscope

# 仅在 .venv 尚不存在时创建
uv venv --python 3.11

source .venv/bin/activate
uv pip install -e .
```

`-e` 是 editable 安装，Python 会直接使用当前仓库的 `src/agentscope` 源码；修改源码后通常不需要重新安装。

基础源码包不包含 Agent Service、Redis 和 RAG 的可选依赖。这个示例使用了 FastAPI、RedisStorage 和 QdrantStore，因此需要在同一个虚拟环境中补装对应 extra：

```bash
source .venv/bin/activate
uv pip install -e ".[service,storage,rag]"
```

验证 AgentScope 确实来自当前源码目录：

```bash
source .venv/bin/activate
python - <<'PY'
import agentscope

print(agentscope.__version__)
print(agentscope.__file__)
PY
```

第二行应指向当前仓库的 `src/agentscope/__init__.py`。

## 4. 安装 Web UI 依赖

该目录是 pnpm workspace，包含 `frontend` 和 `backend` 两个包：

```bash
cd /root/code/agentscope/fly-docs/examples/web_ui
pnpm install --frozen-lockfile
```

如果正在主动更新依赖锁文件，可改用 `pnpm install`；普通安装和 CI/部署建议保留 `--frozen-lockfile`，避免依赖版本漂移。

验证前后端均能完成生产构建：

```bash
pnpm build
```

构建产物分别位于：

- 前端：`frontend/dist/`
- 后端：`backend/dist/`

前端构建时可能出现单个 JavaScript chunk 超过 500 kB 的警告。这是体积优化提示，不会导致构建失败。

## 5. 本地开发启动

建议分别打开三个终端。所有命令都从仓库根目录或示例目录明确执行，避免加载错误的虚拟环境。

### 5.1 启动 Redis

使用 Docker：

```bash
docker run -d \
  --name agentscope-redis \
  --restart unless-stopped \
  -p 6379:6379 \
  -v agentscope-redis-data:/data \
  redis:7-alpine redis-server --appendonly yes
```

检查 Redis：

```bash
docker exec agentscope-redis redis-cli ping
```

预期输出为 `PONG`。

如果已有名为 `agentscope-redis` 的容器，可直接启动：

```bash
docker start agentscope-redis
```

macOS 若没有 Docker，可用 Homebrew 安装本机 Redis：

```bash
brew install redis
```

一次性后台启动（与启动脚本在无 Docker 时的行为一致）：

```bash
mkdir -p /tmp/agentscope-example-$UID/redis-data \
  /tmp/agentscope-example-$UID/logs
redis-server \
  --daemonize yes \
  --port 6379 \
  --dir /tmp/agentscope-example-$UID/redis-data \
  --appendonly yes \
  --pidfile /tmp/agentscope-example-$UID/redis.pid \
  --logfile /tmp/agentscope-example-$UID/logs/redis.log
```

也可以交给 brew 托管（开机可自启）：

```bash
brew services start redis
```

检查本机 Redis：

```bash
redis-cli ping
```

预期输出同样为 `PONG`。使用 `./fly-docs/start_agent_service_web_ui.sh start` 时，若未检测到 Docker 但本机有 `redis-server`，脚本会自动按上述方式启动 Redis。

### 5.2 启动 Agent Service

```bash
cd /root/code/agentscope
source .venv/bin/activate
cd fly-docs/examples/agent_service
python main.py
```

开发模式默认监听 `0.0.0.0:8000`，且开启自动重载。检查服务：

```bash
curl -I http://127.0.0.1:8000/openapi.json
```

返回 `HTTP/1.1 200 OK` 即表示 FastAPI 已启动。也可以在浏览器打开 `http://127.0.0.1:8000/docs` 查看接口文档。

示例默认通过 `npx @playwright/mcp@latest` 注册浏览器 MCP。首次真正使用该 MCP 时可能需要联网下载 npm 包。高德地图 MCP 是可选功能，启用方式如下：

```bash
export AMAP_API_KEY="你的密钥"
python main.py
```

### 5.3 启动 Web UI

新开终端：

```bash
cd /root/code/agentscope/fly-docs/examples/web_ui
pnpm dev
```

该命令并行启动：

- 前端：`http://127.0.0.1:5173`
- Node.js 后端：`http://127.0.0.1:3000`

检查：

```bash
curl -I http://127.0.0.1:5173/
curl http://127.0.0.1:3000/api/health
```

第二条命令预期返回：

```json
{"status":"ok"}
```

若 3000 端口已被占用，只启动前端即可：

```bash
pnpm --filter frontend dev --host 0.0.0.0
```

### 5.4 首次配置 Web UI

打开 `http://127.0.0.1:5173`，在初始化页面填写：

- Server URL：`http://127.0.0.1:8000`
- Username：任意稳定的用户标识，例如 `admin`

如果浏览器和服务不在同一台机器，不能填写浏览器自身的 `127.0.0.1`，必须填写浏览器可以访问的服务器 IP 或域名，例如 `http://192.168.1.20:8000`。

要重新进入配置页，可访问 `/setup`；配置保存在浏览器的 `localStorage` 中。

## 6. 一键验证

所有服务启动后执行：

```bash
curl --fail --silent --show-error \
  http://127.0.0.1:8000/openapi.json >/dev/null \
  && echo "Agent Service: OK"

curl --fail --silent --show-error \
  http://127.0.0.1:3000/api/health \
  && echo

curl --fail --silent --show-error \
  http://127.0.0.1:5173/ >/dev/null \
  && echo "Web UI: OK"
```

本次实测结果：Agent Service OpenAPI 返回 HTTP 200 并包含 32 条路由，Web UI 后端健康检查返回 HTTP 200，前端首页返回 HTTP 200。

## 7. 生产部署建议

生产环境不要使用 `python main.py` 的 `reload=True`，也不要使用 Vite 开发服务器。推荐：

1. Redis 使用持久化磁盘，并限制为内网访问。
2. Agent Service 由 systemd 管理，用 Uvicorn 单进程启动。
3. Web UI 前端执行 `pnpm build` 后由 Nginx 托管。
4. Nginx 为 Agent Service 提供 HTTPS 反向代理。
5. Web UI 中填写 HTTPS API 地址，避免浏览器 mixed content 拦截。

当前示例使用 `InMemoryMessageBus`，只适合单进程。若要多进程或多副本部署，先按 `main.py` 内注释切换成 `RedisMessageBus`，再增加进程或实例数量。

### 7.1 systemd 管理 Agent Service

创建 `/etc/systemd/system/agentscope-agent.service`：

```ini
[Unit]
Description=AgentScope Agent Service
After=network.target docker.service

[Service]
Type=simple
User=agentscope
Group=agentscope
WorkingDirectory=/opt/agentscope/fly-docs/examples/agent_service
Environment=PYTHONUNBUFFERED=1
# 可选：Environment=AMAP_API_KEY=替换为实际密钥
ExecStart=/opt/agentscope/.venv/bin/uvicorn main:app --host 127.0.0.1 --port 8000
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

把 `/opt/agentscope` 和运行用户替换为实际值，然后执行：

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now agentscope-agent
sudo systemctl status agentscope-agent
journalctl -u agentscope-agent -f
```

`main.py` 当前把 Redis 写为 `localhost:6379`。如果 Redis 位于其他主机，应先把连接地址改为环境变量配置，再部署服务；不要把公网 Redis 地址和密码硬编码进仓库。

### 7.2 构建并发布 Web UI

```bash
cd /opt/agentscope/fly-docs/examples/web_ui
pnpm install --frozen-lockfile
pnpm build
```

将 `frontend/dist/` 作为 Nginx 静态站点目录。Node.js 后端目前只提供示例健康检查；若生产环境不需要 `/api/health`，可以不部署它。

### 7.3 Nginx 示例

前端请求的接口路径以 `/` 开头，浏览器的 `new URL()` 会忽略 Server URL 中自定义的子路径。因此不应把 API 部署到 `/agent-api/`；推荐为 API 使用独立子域名。

```nginx
server {
    listen 80;
    server_name agentscope.example.com;

    root /opt/agentscope/fly-docs/examples/web_ui/frontend/dist;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }
}

server {
    listen 80;
    server_name api.agentscope.example.com;

    location / {
        proxy_pass http://127.0.0.1:8000/;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_buffering off;
        proxy_read_timeout 3600s;
    }
}
```

配置后检查并重载：

```bash
sudo nginx -t
sudo systemctl reload nginx
```

Web UI 的 Server URL 填写 `http://api.agentscope.example.com`。启用 TLS 后应改成 `https://api.agentscope.example.com`。

## 8. 停止服务

使用启动脚本时：

```bash
./fly-docs/start_agent_service_web_ui.sh stop
```

这会停止 Agent Service 与 Web UI，并尝试回收相关端口上的残留进程；**默认保留 Redis**。

本地开发若是前台启动，在对应终端按 `Ctrl+C`。

停止 Docker Redis：

```bash
docker stop agentscope-redis
```

停止本机 Redis（macOS / Homebrew 或脚本拉起的 `redis-server`）：

```bash
redis-cli shutdown
# 或
brew services stop redis
```

systemd 部署：

```bash
sudo systemctl stop agentscope-agent
```

## 9. 常见问题

### 9.1 `python: command not found`

系统可能只有 `python3`，而 `.venv` 中才有 `python`。先回到源码根目录并激活环境：

```bash
cd /root/code/agentscope
source .venv/bin/activate
python --version
```

### 9.2 缺少 FastAPI、Redis 或 Qdrant 模块

`uv pip install -e .` 只安装基础依赖。补装本示例需要的源码 extra：

```bash
source .venv/bin/activate
uv pip install -e ".[service,storage,rag]"
```

### 9.3 Redis 连接失败

若使用 Docker：

```bash
docker ps --filter name=agentscope-redis
docker logs agentscope-redis
docker exec agentscope-redis redis-cli ping
```

若使用本机 Redis（常见于 macOS 无 Docker）：

```bash
redis-cli ping
lsof -nP -iTCP:6379 -sTCP:LISTEN
# 日志（由启动脚本拉起时）
tail -n 50 /tmp/agentscope-example-$UID/logs/redis.log
```

预期 `redis-cli ping` 返回 `PONG`。示例默认连接 `localhost:6379`，因此 Redis 必须能从 Agent Service 所在主机通过该地址访问。

### 9.4 端口已被占用

Linux：

```bash
ss -ltnp | grep -E ':(3000|5173|6379|8000)'
```

macOS：

```bash
lsof -nP -iTCP:3000,5173,6379,8000 -sTCP:LISTEN
```

不要直接杀死来源不明的进程。先用 `ps -fp <PID>`（Linux 还可看 `/proc/<PID>/cwd`）确认进程属于哪个项目，再决定停止或改端口。

若确认是本示例残留进程，优先：

```bash
./fly-docs/start_agent_service_web_ui.sh stop
./fly-docs/start_agent_service_web_ui.sh start
```

当前启动脚本在 `stop` / `restart` 时，即使 PID 文件丢失，也会尝试回收 8000 / 3000 / 5173 上的残留监听进程。

### 9.5 Web UI 打开但请求失败

依次检查：

1. 浏览器中保存的 Server URL 是否能从浏览器所在机器访问。
2. `http://服务地址:8000/openapi.json` 是否返回 200。
3. HTTP 页面是否请求了 HTTPS API，或 HTTPS 页面是否请求了 HTTP API。
4. 反向代理路径末尾是否缺少 `/`。
5. 浏览器开发者工具 Network 和 Console 中的具体错误。

示例的 Agent Service 已配置宽松 CORS，适合本地体验。正式上线应把 `allow_origins=["*"]` 收紧为实际 Web UI 域名。

### 9.6 pnpm 安装或构建异常

确认 Node.js 版本不低于 20，并使用锁文件声明的 pnpm（`packageManager` 为 `pnpm@11.12.0`）：

```bash
node --version
corepack enable
corepack install
pnpm --version
pnpm install --frozen-lockfile
pnpm build
```

若本机没有 `corepack`，先执行 `npm install -g pnpm@11.12.0`，再继续 `pnpm install` / `pnpm build`。

后台启动或 `restart` 时若出现 `ERR_PNPM_ABORTED_REMOVE_MODULES_DIR_NO_TTY` / `Exit status 143`，见 [9.8](#98-restart-后-web-ui-失败exit-status-143--err_pnpm_aborted_remove_modules_dir_no_tty)。非交互重装可显式加 `CI=true`：

```bash
cd fly-docs/examples/web_ui
CI=true pnpm install --frozen-lockfile
```

### 9.7 `command not found: setsid`（macOS）

`setsid` 来自 Linux 的 util-linux，Homebrew Node / macOS 默认不提供。当前 `start_agent_service_web_ui.sh` 已改为用 Python `os.setsid()` 创建后台会话，**无需再安装 setsid**。若仍看到该错误，说明脚本不是仓库里的最新版本，请更新 `fly-docs/start_agent_service_web_ui.sh` 后重试：

```bash
./fly-docs/start_agent_service_web_ui.sh start
```

### 9.8 `restart` 后 Web UI 失败：`Exit status 143` / `ERR_PNPM_ABORTED_REMOVE_MODULES_DIR_NO_TTY`

典型日志片段：

```text
Server running on http://localhost:3000
[ERR_PNPM_RECURSIVE_RUN_FIRST_FAIL] backend@1.0.0 dev: ...
Exit status 143
[ERR_PNPM_ABORTED_REMOVE_MODULES_DIR_NO_TTY] Aborted removal of modules directory due to no TTY
```

含义：

1. `Exit status 143` = 进程收到 `SIGTERM`（128 + 15），常见于 PID 文件丢失后旧进程与新进程冲突，或重启时被脚本回收端口误伤竞态。
2. `ERR_PNPM_ABORTED_REMOVE_MODULES_DIR_NO_TTY` = 后台无 TTY 时 pnpm 想重建 `node_modules` 需要交互确认，被中止。

处理步骤：

```bash
# 1. 停掉脚本管理的进程，并回收残留端口
cd /root/code/agentscope
./fly-docs/start_agent_service_web_ui.sh stop

# 2. 在非交互环境下重装 Web UI 依赖
cd fly-docs/examples/web_ui
CI=true pnpm install --frozen-lockfile

# 3. 重新启动并检查状态
cd /root/code/agentscope
./fly-docs/start_agent_service_web_ui.sh start
./fly-docs/start_agent_service_web_ui.sh status
```

仓库已做的防护：

- `fly-docs/examples/web_ui/.npmrc` 含 `confirm-modules-purge=false`
- 启动脚本后台拉起 `pnpm` 时带 `CI=true`
- `stop` / `restart` 在 PID 文件丢失时仍尝试回收应用端口

若 `status` 中 Backend / Frontend 仍为 `[DOWN]`，查看日志定位：

```bash
./fly-docs/start_agent_service_web_ui.sh logs -n 80 web-backend
./fly-docs/start_agent_service_web_ui.sh logs -n 80 web-frontend
```

## 10. 上线检查清单

- [ ] AgentScope 通过 `.venv` 和 `uv pip install -e .` 从源码安装
- [ ] 已补装 `service,storage,rag` 示例依赖
- [ ] Redis 开启持久化、备份和访问控制
- [ ] Agent Service OpenAPI 健康检查返回 200
- [ ] Web UI `pnpm build` 成功
- [ ] 前端由 Nginx 或等价静态服务器托管
- [ ] API 和 Web UI 使用 HTTPS
- [ ] CORS 限制为实际前端域名
- [ ] 多进程部署前已改用 RedisMessageBus
- [ ] API 密钥通过环境变量或密钥管理服务注入
- [ ] systemd 日志、Redis 容量和磁盘空间已纳入监控
