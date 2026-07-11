# AgentScope 本地安装手册

日期：2026-07-09
参考文档：https://docs.agentscope.io/versions/2.0.5dev/zh/quickstart

## 1. 适用场景

本文用于在本地电脑从 PyPI 或源码安装 AgentScope，并记录安装过程中已经遇到过的环境问题。AgentScope 2.0 要求 Python 3.11 及以上版本。

推荐方案是使用 `uv` 创建项目级虚拟环境。`conda` 不是 AgentScope 的必需依赖，如果本机没有安装或没有配置 `conda`，可以直接跳过 `conda`，使用 `.venv` 完成安装。

## 2. 安装前检查

先确认 Python、Git 和 uv 是否可用：

```bash
python3 --version
git --version
uv --version
```

如果没有安装 `uv`，macOS 可以使用 Homebrew：

```bash
brew install uv
```

也可以使用官方安装脚本：

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

安装后如果 `uv --version` 仍然找不到命令，重新打开终端，或把 uv 的安装目录加入 `PATH`。

## 3. 从 PyPI 安装

适合只使用 AgentScope，不修改源码的情况。

```bash
mkdir -p ~/code/agentscope-demo
cd ~/code/agentscope-demo

uv venv --python 3.11
source .venv/bin/activate

uv pip install agentscope
```

如果需要完整功能依赖，macOS / Linux / zsh 下建议给 extra 加引号，避免 shell 把方括号当成通配符：

```bash
uv pip install "agentscope[full]"
```

## 4. 从源码安装

适合需要阅读源码、二次开发或本地调试的情况。

如果已经有本地源码目录，跳过 `git clone`，直接进入该目录继续执行 `uv venv`。

```bash
cd ~/code
git clone -b main https://github.com/agentscope-ai/agentscope.git
cd agentscope

uv venv --python 3.11
source .venv/bin/activate

uv pip install -e .
```

执行过程

```bash
(fly) ➜  agentscope git:(fly-v2.0.4) ✗ uv venv --python 3.11
source .venv/bin/activate

uv pip install -e .
Using CPython 3.11.15 interpreter at: /opt/homebrew/opt/python@3.11/bin/python3.11
Creating virtual environment at: .venv
Activate with: source .venv/bin/activate
Resolved 87 packages in 15.64s
      Built agentscope @ file:///Users/fly/code/agentscope
Prepared 61 packages in 1m 00s
Installed 87 packages in 186ms
 + agentscope==2.0.4 (from file:///Users/fly/code/agentscope)
 + aiofiles==25.1.0
 + aiohappyeyeballs==2.7.1
 + aiohttp==3.14.1
 + aioitertools==0.13.0
 + aiosignal==1.4.0
 + annotated-doc==0.0.4
 + annotated-types==0.7.0
 + anthropic==0.116.0
 + anyio==4.14.1
 + attrs==26.1.0
 + bidict==0.23.1
 + cached-property==2.0.1
 + certifi==2026.6.17
 + cffi==2.1.0
 + charset-normalizer==3.4.9
 + click==8.4.2
 + cryptography==49.0.0
 + dashscope==1.26.2
 + distro==1.9.0
 + docstring-parser==0.18.0
 + filetype==1.2.0
 + frozenlist==1.8.0
 + googleapis-common-protos==1.75.0
 + grpcio==1.82.1
 + h11==0.16.0
 + httpcore==1.0.9
 + httpx==0.28.1
 + httpx-sse==0.4.3
 + idna==3.18
 + jinja2==3.1.6
 + jiter==0.16.0
 + json-repair==0.61.2
 + json5==0.15.0
 + jsonschema==4.26.0
 + jsonschema-specifications==2025.9.1
 + markdown-it-py==4.2.0
 + markupsafe==3.0.3
 + mcp==1.28.1
 + mdurl==0.1.2
 + multidict==6.7.1
 + numpy==2.4.6
 + openai==2.44.0
 + opentelemetry-api==1.43.0
 + opentelemetry-exporter-otlp==1.43.0
 + opentelemetry-exporter-otlp-proto-common==1.43.0
 + opentelemetry-exporter-otlp-proto-grpc==1.43.0
 + opentelemetry-exporter-otlp-proto-http==1.43.0
 + opentelemetry-proto==1.43.0
 + opentelemetry-sdk==1.43.0
 + opentelemetry-semantic-conventions==0.64b0
 + propcache==0.5.2
 + protobuf==7.35.1
 + pycparser==3.0
 + pydantic==2.13.4
 + pydantic-core==2.46.4
 + pydantic-settings==2.14.2
 + pygments==2.20.0
 + pyjwt==2.13.0
 + python-datauri==3.0.2
 + python-dotenv==1.2.2
 + python-engineio==4.13.3
 + python-frontmatter==1.3.0
 + python-multipart==0.0.32
 + python-socketio==5.16.3
 + pyyaml==6.0.3
 + referencing==0.37.0
 + requests==2.34.2
 + rich==15.0.0
 + rpds-py==2026.6.3
 + shellingham==1.5.4
 + shortuuid==1.0.13
 + simple-websocket==1.1.0
 + sniffio==1.3.1
 + sse-starlette==3.4.5
 + starlette==1.3.1
 + tqdm==4.68.4
 + tree-sitter==0.26.0
 + tree-sitter-bash==0.25.1
 + typer==0.26.8
 + typing-extensions==4.16.0
 + typing-inspection==0.4.2
 + urllib3==2.7.0
 + uvicorn==0.51.0
 + websocket-client==1.9.0
 + wsproto==1.3.2
 + yarl==1.24.2
(agentscope) ➜  agentscope git:(fly-v2.0.4) ✗
```

上面的 `uv pip install -e .` 是基础源码安装。如果只是运行和调试基础包，到这里就够了。

如果要开发 AgentScope 本身，建议在同一个已经激活的 `.venv` 中安装开发依赖。开发场景下可以直接把基础安装命令替换为下面的命令，不需要先执行 `uv pip install -e .` 再执行 `uv pip install -e ".[dev]"`：

```bash
uv pip install -e ".[dev]"
pre-commit install
```

如果已经执行过 `uv pip install -e .`，也可以继续执行 `uv pip install -e ".[dev]"` 来补装开发依赖。`uv` 会复用当前激活的 `.venv`。

这里的 `-e` 表示以 editable 模式安装，修改本地源码后不需要重新安装，Python 会直接使用当前源码目录。

`.[dev]` 表示安装当前项目，并额外安装 `pyproject.toml` 中定义的开发依赖，例如 `pytest`、`pre-commit`、文档工具链以及完整功能依赖。

引号用于避免 zsh 把 `[dev]` 当作通配符解析。

`pre-commit install` 会把代码检查钩子注册到当前 Git 仓库，之后每次执行 `git commit` 时会自动运行项目配置的提交前检查。

如果当前机器还没有 Python 3.11，可以先让 uv 安装 Python：

```bash
uv python install 3.11
uv venv --python 3.11
source .venv/bin/activate
```

## 5. 验证安装

安装完成后运行：

```bash
python - <<'PY'
import agentscope

print(agentscope.__version__)
PY
```

能正常打印版本号，说明当前虚拟环境已经可以导入 AgentScope。

## 6. 常见问题

### 6.1 `zsh: command not found: conda`

现象：

```bash
zsh: command not found: conda
```

原因通常是：

- 本机没有安装 Miniconda / Anaconda / Miniforge。
- 已安装 conda，但 shell 没有初始化，`conda` 不在当前 `PATH` 中。

处理建议：

- 如果只是安装 AgentScope，不需要处理 `conda`，直接使用 `uv venv` 创建 `.venv` 即可。
- 如果必须使用 conda，再单独安装 Miniconda / Miniforge，并执行对应的 shell 初始化命令。

AgentScope 的推荐安装路径如下：

```bash
cd ~/code/agentscope
uv venv --python 3.11
source .venv/bin/activate
uv pip install -e .
```

### 6.2 `uv pip install -e .` 提示没有虚拟环境

现象：

```bash
uv pip install -e .
error: No virtual environment found; run `uv venv` to create an environment, or pass `--system` to install into a non-virtual environment
```

原因是 `uv pip` 默认安装到虚拟环境中。当前目录或上级目录没有可用的 `.venv`，并且当前 shell 也没有激活其他虚拟环境。

处理方式：

```bash
cd ~/code/agentscope
uv venv --python 3.11
source .venv/bin/activate
uv pip install -e .
```

错误信息里提到的 `--system` 会把包安装到系统 Python 环境中。除非非常明确需要全局安装，否则不建议在项目开发中使用 `--system`，避免污染系统环境或影响其他项目。

### 6.3 zsh 下安装 extra 时报通配符错误

如果执行下面命令：

```bash
uv pip install agentscope[full]
```

zsh 可能把 `[full]` 解析成文件名通配符。推荐写成：

```bash
uv pip install "agentscope[full]"
```

源码开发时同理：

```bash
uv pip install -e ".[dev]"
```

### 6.4 `git commit` 时 mypy 报 `Duplicate module named "main"`

现象：

```text
mypy.....................................................................Failed
- hook id: mypy
- exit code: 2

fly-docs/examples/.../main.py: error: Duplicate module named "main"
(also at "fly-docs/examples/.../main.py")
```

原因：

- **mypy** 是 Python 静态类型检查工具，本仓库通过 pre-commit 在每次 `git commit` 时自动运行。
- mypy 默认按文件名推断模块名。多个目录下都有 `main.py` 时，会被当成同一个模块 `main`，从而报 Duplicate module。
- 官方文档目录 `docs/` 已在 `.pre-commit-config.yaml` 中被 mypy / flake8 / pylint 排除；本地补充文档目录 `fly-docs/` 若未同步排除，提交其中的示例 Python 文件就会触发该错误。

处理方式：

在 `.pre-commit-config.yaml` 中，把 `fly-docs` 与 `docs` 一样加入排除规则，例如：

```yaml
# mypy
exclude:
    (?x)(
        pb2\.py$
        | grpc\.py$
        | ^docs
        | ^fly-docs
        | \.html$
    )

# flake8
exclude: ^(docs|fly-docs)

# pylint
exclude:
    (?x)(
        ^docs
        | ^fly-docs
        | ...
    )
```

修改后重新 stage 再提交：

```bash
git add .pre-commit-config.yaml
git commit
```

经验：向仓库新增文档目录（尤其是带示例 `.py` 的目录）时，应同步检查 pre-commit 的 exclude 是否需要覆盖该目录，避免文档示例与正式包代码共用同一套类型检查规则。

### 6.5 `pnpm: command not found`

在 `fly-docs/examples/web_ui` 下执行依赖安装时：

```bash
cd ~/code/agentscope/fly-docs/examples/web_ui
pnpm install
```

可能出现：

```text
Command 'pnpm' not found, did you mean:
  command 'npm' from deb npm (...)
```

原因是本机已有 Node.js / npm，但尚未安装或启用 `pnpm`。该示例使用 pnpm workspace，不能改用 `npm install` 替代。

推荐用 Node.js 自带的 Corepack 启用 pnpm：

```bash
corepack enable
corepack prepare pnpm@latest --activate
pnpm --version
```

如果 `corepack` 不可用，也可以用 npm 全局安装：

```bash
npm install -g pnpm
pnpm --version
```

确认 `pnpm --version` 可用后，再回到示例目录安装依赖：

```bash
cd ~/code/agentscope/fly-docs/examples/web_ui
pnpm install
```

如果连 `node` / `npm` 都没有，需要先安装 Node.js（建议 20 及以上），再按上面步骤启用 pnpm。

## 7. 推荐排障顺序

遇到安装问题时，按下面顺序检查：

1. 确认当前目录：源码安装时必须先进入 `~/code/agentscope` 这类源码根目录。
2. 确认 Python 版本：`python --version` 或 `python3 --version` 应为 3.11 及以上。
3. 确认虚拟环境：项目根目录应存在 `.venv`，或当前终端已执行 `source .venv/bin/activate`。
4. 确认安装命令：普通使用安装 `agentscope`，源码开发安装 `-e .`，开发测试安装 `-e ".[dev]"`。
5. 再次验证导入：使用第 5 节的 Python 命令确认 `import agentscope` 是否成功。
