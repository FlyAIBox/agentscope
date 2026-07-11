#!/usr/bin/env bash

set -Eeuo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "${SCRIPT_DIR}/.." && pwd)"
AGENT_DIR="${REPO_ROOT}/fly-docs/examples/agent_service"
WEB_DIR="${REPO_ROOT}/fly-docs/examples/web_ui"
VENV_DIR="${REPO_ROOT}/.venv"
RUN_DIR="${XDG_RUNTIME_DIR:-/tmp}/agentscope-example-${UID}"
LOG_DIR="${RUN_DIR}/logs"

REDIS_CONTAINER="${REDIS_CONTAINER:-agentscope-redis}"
REDIS_PORT="${REDIS_PORT:-6379}"
AGENT_PORT="${AGENT_PORT:-8000}"
WEB_BACKEND_PORT="${WEB_BACKEND_PORT:-3000}"
WEB_FRONTEND_PORT="${WEB_FRONTEND_PORT:-5173}"

mkdir -p "${LOG_DIR}"

info() { printf '[INFO] %s\n' "$*"; }
warn() { printf '[WARN] %s\n' "$*" >&2; }
fail() { printf '[ERROR] %s\n' "$*" >&2; exit 1; }

pid_file() { printf '%s/%s.pid' "${RUN_DIR}" "$1"; }
log_file() { printf '%s/%s.log' "${LOG_DIR}" "$1"; }

require_command() {
    command -v "$1" >/dev/null 2>&1 || fail "缺少命令：$1"
}

tcp_open() {
    local port="$1"
    (exec 3<>"/dev/tcp/127.0.0.1/${port}") >/dev/null 2>&1
}

http_ok() {
    curl --fail --silent --show-error --max-time 3 "$1" >/dev/null 2>&1
}

wait_for_url() {
    local name="$1" url="$2" attempts="${3:-30}"
    local i
    for ((i = 1; i <= attempts; i++)); do
        if http_ok "${url}"; then
            info "${name} 已就绪：${url}"
            return 0
        fi
        sleep 1
    done
    warn "${name} 启动超时，日志如下："
    tail -n 40 "$(log_file "${name}")" 2>/dev/null || true
    return 1
}

managed_pid() {
    local name="$1" file pid
    file="$(pid_file "${name}")"
    [[ -f "${file}" ]] || return 1
    pid="$(<"${file}")"
    if [[ "${pid}" =~ ^[0-9]+$ ]] && kill -0 "${pid}" 2>/dev/null; then
        printf '%s' "${pid}"
        return 0
    fi
    rm -f "${file}"
    return 1
}

start_process() {
    local name="$1" workdir="$2"
    shift 2

    local pid
    if pid="$(managed_pid "${name}")"; then
        info "${name} 已由脚本管理（PID ${pid}）"
        return 0
    fi

    info "启动 ${name}，日志：$(log_file "${name}")"
    (
        cd "${workdir}"
        exec setsid "$@" >>"$(log_file "${name}")" 2>&1
    ) &
    pid=$!
    printf '%s\n' "${pid}" >"$(pid_file "${name}")"
    sleep 1

    if ! kill -0 "${pid}" 2>/dev/null; then
        tail -n 40 "$(log_file "${name}")" 2>/dev/null || true
        rm -f "$(pid_file "${name}")"
        fail "${name} 启动失败"
    fi
}

stop_process() {
    local name="$1" pid i
    if ! pid="$(managed_pid "${name}")"; then
        info "${name} 没有脚本管理的运行进程"
        return 0
    fi

    info "停止 ${name}（进程组 ${pid}）"
    kill -TERM -- "-${pid}" 2>/dev/null || kill -TERM "${pid}" 2>/dev/null || true
    for ((i = 1; i <= 10; i++)); do
        kill -0 "${pid}" 2>/dev/null || break
        sleep 1
    done
    if kill -0 "${pid}" 2>/dev/null; then
        warn "${name} 未及时退出，发送 KILL"
        kill -KILL -- "-${pid}" 2>/dev/null || kill -KILL "${pid}" 2>/dev/null || true
    fi
    rm -f "$(pid_file "${name}")"
}

activate_venv() {
    [[ -f "${VENV_DIR}/bin/activate" ]] || fail ".venv 不存在，请先运行：$0 install"
    # shellcheck disable=SC1091
    source "${VENV_DIR}/bin/activate"
}

install_all() {
    require_command uv
    require_command node
    require_command pnpm

    cd "${REPO_ROOT}"
    if [[ ! -f "${VENV_DIR}/bin/activate" ]]; then
        info "创建 Python 3.11 虚拟环境"
        uv venv --python 3.11
    fi

    activate_venv
    info "以 editable 模式安装 AgentScope 源码"
    uv pip install -e .
    info "补装 Agent Service 所需可选依赖"
    uv pip install -e ".[service,storage,rag]"

    info "安装 Web UI 依赖"
    cd "${WEB_DIR}"
    pnpm install --frozen-lockfile
    info "安装完成"
}

check_runtime_dependencies() {
    require_command curl
    require_command setsid
    require_command node
    require_command pnpm
    activate_venv

    python - <<'PY' >/dev/null || fail "Python 依赖不完整，请运行启动脚本的 install 命令"
import agentscope
import fastapi
import qdrant_client
import redis
import uvicorn
PY

    [[ -d "${WEB_DIR}/node_modules" ]] || fail "Web UI 依赖未安装，请运行：$0 install"
}

start_redis() {
    if tcp_open "${REDIS_PORT}"; then
        info "Redis 端口已就绪：127.0.0.1:${REDIS_PORT}"
        return 0
    fi

    require_command docker
    if docker container inspect "${REDIS_CONTAINER}" >/dev/null 2>&1; then
        info "启动已有 Redis 容器：${REDIS_CONTAINER}"
        docker start "${REDIS_CONTAINER}" >/dev/null
    else
        info "创建 Redis 容器：${REDIS_CONTAINER}"
        docker run -d \
            --name "${REDIS_CONTAINER}" \
            --restart unless-stopped \
            -p "${REDIS_PORT}:6379" \
            -v agentscope-redis-data:/data \
            redis:7-alpine redis-server --appendonly yes >/dev/null
    fi

    local i
    for ((i = 1; i <= 20; i++)); do
        tcp_open "${REDIS_PORT}" && { info "Redis 已就绪：127.0.0.1:${REDIS_PORT}"; return 0; }
        sleep 1
    done
    fail "Redis 启动超时"
}

start_all() {
    check_runtime_dependencies
    start_redis

    if http_ok "http://127.0.0.1:${AGENT_PORT}/openapi.json"; then
        info "Agent Service 已在运行：http://127.0.0.1:${AGENT_PORT}"
    elif tcp_open "${AGENT_PORT}"; then
        fail "端口 ${AGENT_PORT} 已被其他服务占用"
    else
        start_process agent-service "${AGENT_DIR}" \
            "${VENV_DIR}/bin/python" main.py
        wait_for_url agent-service "http://127.0.0.1:${AGENT_PORT}/openapi.json"
    fi

    if http_ok "http://127.0.0.1:${WEB_BACKEND_PORT}/api/health"; then
        info "Web UI Backend 已在运行：http://127.0.0.1:${WEB_BACKEND_PORT}"
    elif tcp_open "${WEB_BACKEND_PORT}"; then
        fail "端口 ${WEB_BACKEND_PORT} 已被其他服务占用"
    else
        start_process web-backend "${WEB_DIR}" \
            pnpm --filter backend dev
        wait_for_url web-backend "http://127.0.0.1:${WEB_BACKEND_PORT}/api/health"
    fi

    if http_ok "http://127.0.0.1:${WEB_FRONTEND_PORT}/"; then
        info "Web UI Frontend 已在运行：http://127.0.0.1:${WEB_FRONTEND_PORT}"
    elif tcp_open "${WEB_FRONTEND_PORT}"; then
        fail "端口 ${WEB_FRONTEND_PORT} 已被其他服务占用"
    else
        start_process web-frontend "${WEB_DIR}" \
            pnpm --filter frontend dev --host 0.0.0.0
        wait_for_url web-frontend "http://127.0.0.1:${WEB_FRONTEND_PORT}/"
    fi

    printf '\n'
    info "全部服务已启动"
    printf '  Web UI:       http://127.0.0.1:%s\n' "${WEB_FRONTEND_PORT}"
    printf '  Agent API:    http://127.0.0.1:%s\n' "${AGENT_PORT}"
    printf '  API 文档:     http://127.0.0.1:%s/docs\n' "${AGENT_PORT}"
    printf '  运行日志:     %s\n' "${LOG_DIR}"
}

stop_all() {
    stop_process web-frontend
    stop_process web-backend
    stop_process agent-service
    info "Redis 默认保留运行，以免影响数据；如需停止请执行：docker stop ${REDIS_CONTAINER}"
}

show_status() {
    local failed=0
    if tcp_open "${REDIS_PORT}"; then
        printf '[UP]   Redis              127.0.0.1:%s\n' "${REDIS_PORT}"
    else
        printf '[DOWN] Redis              127.0.0.1:%s\n' "${REDIS_PORT}"
        failed=1
    fi
    if http_ok "http://127.0.0.1:${AGENT_PORT}/openapi.json"; then
        printf '[UP]   Agent Service      http://127.0.0.1:%s\n' "${AGENT_PORT}"
    else
        printf '[DOWN] Agent Service      http://127.0.0.1:%s\n' "${AGENT_PORT}"
        failed=1
    fi
    if http_ok "http://127.0.0.1:${WEB_BACKEND_PORT}/api/health"; then
        printf '[UP]   Web UI Backend     http://127.0.0.1:%s\n' "${WEB_BACKEND_PORT}"
    else
        printf '[DOWN] Web UI Backend     http://127.0.0.1:%s\n' "${WEB_BACKEND_PORT}"
        failed=1
    fi
    if http_ok "http://127.0.0.1:${WEB_FRONTEND_PORT}/"; then
        printf '[UP]   Web UI Frontend    http://127.0.0.1:%s\n' "${WEB_FRONTEND_PORT}"
    else
        printf '[DOWN] Web UI Frontend    http://127.0.0.1:%s\n' "${WEB_FRONTEND_PORT}"
        failed=1
    fi
    return "${failed}"
}

show_logs() {
    local name="${1:-}"
    if [[ -n "${name}" ]]; then
        case "${name}" in
            agent-service|web-backend|web-frontend) ;;
            *) fail "未知服务：${name}" ;;
        esac
        touch "$(log_file "${name}")"
        tail -n 100 -f "$(log_file "${name}")"
    else
        info "日志目录：${LOG_DIR}"
        for name in agent-service web-backend web-frontend; do
            printf '\n===== %s =====\n' "${name}"
            tail -n 30 "$(log_file "${name}")" 2>/dev/null || true
        done
    fi
}

usage() {
    cat <<EOF
用法：$(basename "$0") <命令>

命令：
  install              安装源码、Python extra 和 Web UI 依赖
  start                启动 Redis、Agent Service 和 Web UI
  stop                 停止由本脚本启动的应用进程（保留 Redis）
  restart              重启由本脚本管理的应用进程
  status               检查全部服务状态
  logs [服务名]        查看日志；服务名可为 agent-service、web-backend、web-frontend
  help                 显示帮助

首次使用：
  $(basename "$0") install
  $(basename "$0") start
EOF
}

case "${1:-start}" in
    install) install_all ;;
    start) start_all ;;
    stop) stop_all ;;
    restart) stop_all; start_all ;;
    status) show_status ;;
    logs) show_logs "${2:-}" ;;
    help|-h|--help) usage ;;
    *) usage; fail "未知命令：$1" ;;
esac
