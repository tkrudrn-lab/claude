#!/bin/bash
#
# install_hermes_full.sh — 一键安装 Hermes Agent + TencentDB Memory + Web UI
#
# 支持平台：
#   - macOS（Intel / Apple Silicon）
#   - Ubuntu / Debian（含 WSL2）
#
# 用法：
#   bash <(curl -fsSL https://raw.githubusercontent.com/buer6361/hermes-setup/main/install_hermes_full.sh)
#
#   或下载后本地执行：
#   bash install_hermes_full.sh
#
# 前置条件：
#   - 网络通畅（需下载 Node.js 包、git clone）
#   - sudo 权限（仅 Ubuntu/WSL 需要，用于 apt-get install）
#   - macOS 需已安装 Xcode Command Line Tools（首次运行会自动弹窗）

set -e

# ============================================================
# 颜色
# ============================================================
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

info()  { echo -e "${BLUE}[INFO]${NC} $1"; }
ok()    { echo -e "${GREEN}[OK]${NC} $1"; }
warn()  { echo -e "${YELLOW}[WARN]${NC} $1"; }
err()   { echo -e "${RED}[ERROR]${NC} $1"; }
header(){ echo -e "\n${CYAN}━━━ $1 ━━━${NC}\n"; }

# ============================================================
# 环境检测
# ============================================================
detect_os() {
    case "$(uname -s)" in
        Linux*)
            if grep -qi microsoft /proc/version 2>/dev/null; then
                echo "wsl"
            else
                echo "linux"
            fi
            ;;
        Darwin*) echo "macos" ;;
        *)       echo "unknown" ;;
    esac
}

detect_arch() {
    case "$(uname -m)" in
        x86_64|amd64) echo "amd64" ;;
        aarch64|arm64) echo "arm64" ;;
        *)            echo "$(uname -m)" ;;
    esac
}

OS=$(detect_os)
ARCH=$(detect_arch)
USERNAME=$(whoami)
USER_HOME=$(eval echo ~$USERNAME)

header "环境检测"
info "操作系统: $OS ($ARCH)"
info "用户: $USERNAME"
info "Home: $USER_HOME"

if [ "$OS" = "wsl" ]; then
    info "WSL2 检测到 — Ubuntu 路径会自动适配"
fi

# ============================================================
# Step 0: 安装系统依赖
# ============================================================
install_system_deps() {
    header "Step 0: 安装系统依赖"

    if [ "$OS" = "macos" ]; then
        # macOS — 确保 brew 和 Xcode CLI tools
        if ! xcode-select -p &>/dev/null; then
            info "安装 Xcode Command Line Tools..."
            xcode-select --install
            warn "请等待 Xcode CLI Tools 安装完成后重新运行此脚本"
            exit 0
        fi

        if ! command -v brew &>/dev/null; then
            info "安装 Homebrew..."
            NONINTERACTIVE=1 /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

            # 配置 brew PATH（Apple Silicon 需要）
            if [ "$ARCH" = "arm64" ]; then
                echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> "$USER_HOME/.zprofile"
                eval "$(/opt/homebrew/bin/brew shellenv)"
            fi
            ok "Homebrew 安装完成"
        fi

        brew install git python@3.11 node@22
        ok "系统依赖安装完成"

    elif [ "$OS" = "linux" ] || [ "$OS" = "wsl" ]; then
        # Ubuntu / Debian / WSL
        sudo apt-get update -qq
        sudo apt-get install -y -qq curl git python3 python3-pip python3-venv \
            build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev \
            libsqlite3-dev libffi-dev libgdbm-dev liblzma-dev tk-dev
        ok "系统依赖安装完成"
    fi
}

# ============================================================
# Step 1: 安装 Node.js
# ============================================================
install_nodejs() {
    header "Step 1: 安装 Node.js"

    if command -v node &>/dev/null; then
        NODE_VER=$(node --version 2>/dev/null | sed 's/v//' | cut -d. -f1)
        if [ "$NODE_VER" -ge 18 ] 2>/dev/null; then
            ok "Node.js $(node --version) 已安装"
            return 0
        fi
    fi

    if [ "$OS" = "macos" ]; then
        brew install node@22
        brew link --overwrite node@22

    elif [ "$OS" = "linux" ] || [ "$OS" = "wsl" ]; then
        # 使用 nvm 安装 Node 22
        export NVM_DIR="$USER_HOME/.nvm"
        if [ ! -s "$NVM_DIR/nvm.sh" ]; then
            curl -fsSL https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash
        fi
        [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"

        nvm install 22
        nvm use 22
        nvm alias default 22

        # 写入 bashrc/zshrc
        for rc in "$USER_HOME/.bashrc" "$USER_HOME/.zshrc"; do
            if [ -f "$rc" ] && ! grep -q 'nvm.sh' "$rc" 2>/dev/null; then
                echo 'export NVM_DIR="$HOME/.nvm"' >> "$rc"
                echo '[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"' >> "$rc"
                ok "nvm 已写入 $rc"
            fi
        done
    fi

    ok "Node.js $(node --version) 安装完成"
}

# ============================================================
# Step 2: 安装 Hermes Agent
# ============================================================
install_hermes() {
    header "Step 2: 安装 Hermes Agent"

    if command -v hermes &>/dev/null; then
        HERMES_VER=$(hermes --version 2>/dev/null | head -1)
        ok "Hermes Agent 已安装 ($HERMES_VER)"
        return 0
    fi

    curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash

    # 确保 hermes 在 PATH 中
    export PATH="$USER_HOME/.local/bin:$PATH"
    if command -v hermes &>/dev/null; then
        ok "Hermes Agent $(hermes --version | head -1) 安装完成"
    else
        err "hermes 安装后未在 PATH 中找到"
        err "请手动添加 ~/.local/bin 到 PATH"
        return 1
    fi
}

# ============================================================
# Step 3: 基础配置
# ============================================================
setup_hermes() {
    header "Step 3: 配置 Hermes 基础设置"

    hermes doctor --fix 2>/dev/null || true

    if ! hermes profile list 2>/dev/null | grep -q -E "default|◆"; then
        hermes profile create default 2>/dev/null || true
        ok "已创建 default profile"
    fi

    # 启用必要的工具集
    hermes tools enable skills 2>/dev/null || true
    hermes tools enable memory 2>/dev/null || true

    ok "Hermes 基础配置完成"
    warn "运行 hermes model 或 hermes setup 选择模型和配置 API Key"
}

# ============================================================
# Step 4: 安装 TencentDB Agent Memory
# ============================================================
install_tdai_memory() {
    header "Step 4: 安装 TencentDB Agent Memory"

    MEMORY_ROOT="$USER_HOME/.memory-tencentdb"
    TDAI_DIR="$MEMORY_ROOT/tdai-memory-openclaw-plugin"
    DATA_DIR="$MEMORY_ROOT/memory-tdai"

    # 重复安装保护
    if [ -d "$TDAI_DIR/node_modules" ] && [ -f "$TDAI_DIR/dist/index.mjs" ]; then
        ok "TencentDB Memory 已安装"
        info "  位置: $TDAI_DIR"
        return 0
    fi

    mkdir -p "$MEMORY_ROOT"

    # 通过 npm 下载
    info "  下载 @tencentdb-agent-memory/memory-tencentdb..."
    TEMP_DIR=$(mktemp -d /tmp/tdai-download-XXXXXX)
    cd "$TEMP_DIR"
    npm init -y --silent > /dev/null 2>&1
    npm install @tencentdb-agent-memory/memory-tencentdb@latest --omit=dev 2>&1 | tail -3

    PACK_DIR="$TEMP_DIR/node_modules/@tencentdb-agent-memory/memory-tencentdb"
    if [ ! -d "$PACK_DIR" ]; then
        err "包下载失败"
        rm -rf "$TEMP_DIR"
        return 1
    fi

    rm -rf "$TDAI_DIR"
    cp -r "$PACK_DIR" "$TDAI_DIR"

    # 安装 Gateway 依赖
    info "  安装 Gateway Node.js 依赖..."
    cd "$TDAI_DIR"
    npm install --omit=dev 2>&1 | tail -3
    npm install tsx 2>&1 | tail -2

    # 初始化数据目录
    mkdir -p "$DATA_DIR"/{conversations,records,scene_blocks}
    ok "  数据目录: $DATA_DIR"

    # 将插件链接到 Hermes 插件系统
    HERMES_AGENT_DIR="$USER_HOME/.hermes/hermes-agent"
    HERMES_PLUGIN_DIR="$HERMES_AGENT_DIR/plugins/memory/memory_tencentdb"
    PLUGIN_SRC="$TDAI_DIR/hermes-plugin/memory/memory_tencentdb"

    if [ -d "$PLUGIN_SRC" ]; then
        rm -rf "$HERMES_PLUGIN_DIR"
        ln -sf "$PLUGIN_SRC" "$HERMES_PLUGIN_DIR"
        ok "  插件已链接到 $HERMES_PLUGIN_DIR"
    else
        warn "  插件目录不存在: $PLUGIN_SRC（新版本可能移除了 hermes-plugin）"
    fi

    # 写入环境变量
    GATEWAY_CMD="sh -c 'cd $TDAI_DIR && exec npx tsx src/gateway/server.ts'"
    HERMES_ENV="$USER_HOME/.hermes/.env"
    [ ! -f "$HERMES_ENV" ] && touch "$HERMES_ENV"

    for pair in \
        "MEMORY_TENCENTDB_GATEWAY_CMD=$GATEWAY_CMD" \
        "MEMORY_TENCENTDB_GATEWAY_HOST=127.0.0.1" \
        "MEMORY_TENCENTDB_GATEWAY_PORT=8420"; do
        key="${pair%%=*}"
        value="${pair#*=}"
        sed -i "/^${key}=/d" "$HERMES_ENV" 2>/dev/null || true
        echo "${key}=\"${value}\"" >> "$HERMES_ENV"
    done

    # 启用 memory_tencentdb 提供者
    hermes config set memory.provider memory_tencentdb 2>/dev/null || true
    hermes config set memory.memory_enabled true 2>/dev/null || true
    hermes config set memory.user_profile_enabled true 2>/dev/null || true

    rm -rf "$TEMP_DIR"

    ok "TencentDB Memory 安装完成"
    warn "请配置 LLM API Key（记忆提取使用）："
    echo ""
    echo "   编辑 $HERMES_ENV，添加："
    echo "   MEMORY_TENCENTDB_LLM_API_KEY=sk-你的key"
    echo "   MEMORY_TENCENTDB_LLM_BASE_URL=https://api.deepseek.com"
    echo "   MEMORY_TENCENTDB_LLM_MODEL=deepseek-chat"
    echo ""
}

# ============================================================
# Step 5: 安装 hermes-web-ui
# ============================================================
install_web_ui() {
    header "Step 5: 安装 Hermes Web UI"

    if command -v hermes-web-ui &>/dev/null; then
        VER=$(hermes-web-ui --version 2>/dev/null || echo "?")
        ok "hermes-web-ui 已安装 ($VER)"
        info "  升级到最新版..."
        npm update -g hermes-web-ui 2>/dev/null | tail -2 || true
        return 0
    fi

    npm install -g hermes-web-ui 2>&1 | tail -5

    if command -v hermes-web-ui &>/dev/null; then
        ok "hermes-web-ui 安装完成"
    else
        warn "安装完成但 hermes-web-ui 不在 PATH 中"
        warn "尝试：npx hermes-web-ui start"
    fi
}

# ============================================================
# Step 6: 启动 Gateway
# ============================================================
setup_gateway() {
    header "Step 6: 配置并启动 Gateway"

    hermes gateway setup 2>/dev/null || true
    hermes gateway start 2>/dev/null || true

    # 等待启动
    sleep 2
    if curl -sf http://127.0.0.1:8642/health > /dev/null 2>&1; then
        ok "Gateway 运行中（:8642）"
    else
        warn "Gateway 可能未启动，稍后手动执行：hermes gateway start"
    fi
}

# ============================================================
# 安装总结
# ============================================================
print_summary() {
    echo ""
    echo "╔══════════════════════════════════════════════════════╗"
    echo "║            ${GREEN}  安装完成！${NC}                         ║"
    echo "╚══════════════════════════════════════════════════════╝"
    echo ""

    if [ "$OS" = "wsl" ]; then
        echo -e "${YELLOW}⚠ WSL2 提示${NC}"
        echo "  Gateway 默认绑定 127.0.0.1，如需从 Windows 访问 Web UI："
        echo "    1. 启动 Web UI 时指定 0.0.0.0"
        echo "       hermes-web-ui start --host 0.0.0.0"
        echo "    2. 在 PowerShell 中用下面命令查 WSL IP："
        echo "       wsl hostname -I"
        echo ""
    fi

    echo "━━━ 后续步骤 ━━━"
    echo ""
    echo "1. 配置模型和 API Key："
    echo "   hermes model"
    echo "   # 或手动："
    echo "   hermes config set model.provider <provider>"
    echo "   hermes config set model.default <model>"
    echo ""
    echo "2. 配置消息平台（Telegram/Discord 等）："
    echo "   hermes gateway setup"
    echo ""
    echo "3. 配置 Memory 提取模型的 API Key（编辑 ~/.hermes/.env）："
    echo "   MEMORY_TENCENTDB_LLM_API_KEY=sk-..."
    echo "   MEMORY_TENCENTDB_LLM_BASE_URL=https://api.deepseek.com"
    echo "   MEMORY_TENCENTDB_LLM_MODEL=deepseek-chat"
    echo ""
    echo "4. 启动 Web 管理面판："
    echo "   hermes-web-ui start"
    echo "   → http://localhost:8648"
    echo ""
    echo "5. 开始使用："
    echo "   hermes"
    echo ""
    echo "━━━ 安装路径 ━━━"
    echo "   Hermes:          $USER_HOME/.hermes/"
    echo "   TencentDB Memory: $MEMORY_ROOT"
    echo "   Web UI:          npm global"
    echo ""
    echo "━━━ 常用命令 ━━━"
    echo "   hermes                         # 启动聊天"
    echo "   hermes update                  # 更新到最新版"
    echo "   hermes doctor                  # 检查配置"
    echo "   hermes gateway status          # Gateway 状态"
    echo "   hermes-web-ui start            # 启动 Web 面板"
    echo "   hermes model                   # 切换模型"
    echo ""
}

# ============================================================
# 主流程
# ============================================================
main() {
    echo ""
    echo "╔══════════════════════════════════════════════════════╗"
    echo "║       Hermes Agent 一键安装脚本                      ║"
    echo "║       包含：Hermes + TencentDB Memory + Web UI      ║"
    echo "║       支持：macOS / Ubuntu / WSL2                   ║"
    echo "╚══════════════════════════════════════════════════════╝"
    echo ""

    # 失败时继续
    INSTALL_OK=true

    install_system_deps || warn "Step 0 部分失败，继续..."
    install_nodejs   || warn "Step 1 部分失败，继续..."
    install_hermes   || { warn "Step 2 失败"; INSTALL_OK=false; }
    setup_hermes     || warn "Step 3 部分失败，继续..."
    install_tdai_memory || warn "Step 4 部分失败，继续..."
    install_web_ui   || warn "Step 5 部分失败，继续..."
    setup_gateway    || warn "Step 6 部分失败，继续..."

    if [ "$INSTALL_OK" = true ]; then
        print_summary
    else
        warn "部分步骤未完成，请查看上方错误信息"
    fi
}

# 执行
main "$@"
