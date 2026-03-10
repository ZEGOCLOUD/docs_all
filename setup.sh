#!/bin/bash

# 设置颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}    ZEGO 文档项目环境设置脚本${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# 解析参数
DEV_MODE=false
for arg in "$@"; do
	case "$arg" in
		--dev)
			DEV_MODE=true
			;;
		*)
			;;
	esac
done

# 1. 检查 Node.js 版本
echo -e "${YELLOW}1. 检查 Node.js 版本...${NC}"
if command -v node &> /dev/null; then
    NODE_VERSION=$(node -v | cut -d'v' -f2)
    NODE_MAJOR=$(echo $NODE_VERSION | cut -d'.' -f1)

    echo -e "当前 Node.js 版本: ${GREEN}v$NODE_VERSION${NC}"

    if [ "$NODE_MAJOR" -ge 19 ]; then
        echo -e "${GREEN}✓ Node.js 版本满足要求 (>= 19)${NC}"
    else
        echo -e "${RED}✗ Node.js 版本过低，需要 >= 19，当前版本: $NODE_VERSION${NC}"
        echo -e "${YELLOW}正在安装最新的 LTS 版本...${NC}"

        # 检测操作系统并安装 Node.js
        if [[ "$OSTYPE" == "darwin"* ]]; then
            # macOS
            if command -v brew &> /dev/null; then
                echo "使用 Homebrew 安装 Node.js..."
                brew install node
            else
                echo -e "${RED}请先安装 Homebrew: https://brew.sh/${NC}"
                echo "或者从 https://nodejs.org/ 下载最新的 LTS 版本"
                exit 1
            fi
        elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
            # Linux
            if command -v curl &> /dev/null; then
                echo "使用 NodeSource 安装 Node.js..."
                curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
                sudo apt-get install -y nodejs
            else
                echo -e "${RED}请先安装 curl，然后从 https://nodejs.org/ 下载最新的 LTS 版本${NC}"
                exit 1
            fi
        else
            echo -e "${RED}不支持的操作系统，请手动安装 Node.js >= 19${NC}"
            exit 1
        fi

        # 验证安装
        if command -v node &> /dev/null; then
            NEW_VERSION=$(node -v)
            echo -e "${GREEN}✓ Node.js 安装成功: $NEW_VERSION${NC}"
        else
            echo -e "${RED}✗ Node.js 安装失败${NC}"
            exit 1
        fi
    fi
else
    echo -e "${RED}✗ 未找到 Node.js${NC}"
    echo -e "${YELLOW}正在安装 Node.js...${NC}"

    if [[ "$OSTYPE" == "darwin"* ]]; then
        if command -v brew &> /dev/null; then
            brew install node
        else
            echo -e "${RED}请先安装 Homebrew: https://brew.sh/${NC}"
            exit 1
        fi
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if command -v curl &> /dev/null; then
            curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
            sudo apt-get install -y nodejs
        else
            echo -e "${RED}请先安装 curl${NC}"
            exit 1
        fi
    else
        echo -e "${RED}请从 https://nodejs.org/ 下载并安装 Node.js >= 19${NC}"
        exit 1
    fi
fi

echo ""

# 2. 安装/升级 Docuo CLI
NPM_REGISTRY="--registry=https://registry.npmmirror.com"
echo -e "${YELLOW}2. 检查 Docuo CLI...${NC}"
if command -v docuo &> /dev/null; then
    CURRENT_DOCUO_VERSION=$(npm list -g @spreading/docuo --depth=0 2>/dev/null | grep @spreading/docuo | sed 's/.*@spreading\/docuo@//')
    LATEST_DOCUO_VERSION=$(npm view @spreading/docuo version $NPM_REGISTRY 2>/dev/null)
    echo -e "当前 Docuo CLI 版本: ${GREEN}${CURRENT_DOCUO_VERSION}${NC}"
    echo -e "最新 Docuo CLI 版本: ${GREEN}${LATEST_DOCUO_VERSION}${NC}"

    if [ "$CURRENT_DOCUO_VERSION" = "$LATEST_DOCUO_VERSION" ]; then
        echo -e "${GREEN}✓ Docuo CLI 已是最新版本，无需升级${NC}"
    else
        echo -e "${YELLOW}正在清理旧缓存内容...${NC}"
        docuo clear
        echo -e "${GREEN}✓ 旧缓存已清理${NC}"
        echo -e "${YELLOW}正在升级 Docuo CLI: ${CURRENT_DOCUO_VERSION} -> ${LATEST_DOCUO_VERSION}...${NC}"
        npm install -g @spreading/docuo@latest $NPM_REGISTRY
        echo -e "${GREEN}✓ Docuo CLI 已升级到 ${LATEST_DOCUO_VERSION}${NC}"
    fi
else
    echo -e "${YELLOW}正在安装 Docuo CLI...${NC}"
    npm install -g @spreading/docuo@latest $NPM_REGISTRY

    if command -v docuo &> /dev/null; then
        echo -e "${GREEN}✓ Docuo CLI 安装成功${NC}"
    else
        echo -e "${RED}✗ Docuo CLI 安装失败${NC}"
        echo -e "${YELLOW}请尝试手动安装: npm install -g @spreading/docuo${NC}"
    fi
fi

echo ""

# 以下步骤仅在 --dev 模式下执行
if [ "$DEV_MODE" = true ]; then
	# 3. 复制 Git Hooks
	echo -e "${YELLOW}3. 复制 Git Hooks...${NC}"
	cp -f .hooks/* .git/hooks/
	echo -e "${GREEN}✓ Git Hooks 复制成功${NC}"
	echo ""

	# 4. 提醒安装 VS Code 插件
	echo -e "${YELLOW}4. 推荐的 VS Code 插件:${NC}"
	echo -e "${BLUE}请安装以下插件以获得更好的开发体验:${NC}"
	echo ""
	echo -e "${GREEN}• Docuo:${NC} https://marketplace.visualstudio.com/items?itemName=spreading-docuo.docuo"
	echo -e "${GREEN}• Markdown Table:${NC} https://marketplace.visualstudio.com/items?itemName=TakumiI.markdowntable"
	echo -e "${GREEN}• GitLens:${NC} https://marketplace.visualstudio.com/items?itemName=eamodio.gitlens"
	echo -e "${GREEN}• MDX:${NC} https://marketplace.visualstudio.com/items?itemName=unifiedjs.vscode-mdx"
	echo -e "${GREEN}• GitHub Pull Request:${NC} https://marketplace.visualstudio.com/items?itemName=GitHub.vscode-pull-request-github"
	echo ""

	# 5. 提醒查看详细使用说明
	echo -e "${YELLOW}5. 详细使用说明:${NC}"
	echo -e "${BLUE}请查看详细的使用指南:${NC}"
	echo -e "${GREEN}https://zegocloud.feishu.cn/wiki/G3stwqUPYinrVEkkWkFctzdTnwb${NC}"
	echo ""
fi

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}    环境设置完成！${NC}"
echo -e "${BLUE}========================================${NC}"