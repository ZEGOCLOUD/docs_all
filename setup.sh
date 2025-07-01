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

# 2. 安装 Docuo CLI
echo -e "${YELLOW}2. 安装 Docuo CLI...${NC}"
if command -v docuo &> /dev/null; then
    echo -e "${GREEN}✓ Docuo CLI 已安装${NC}"
else
    echo -e "${YELLOW}正在安装 Docuo CLI...${NC}"
    npm install -g @spreading/docuo
    
    if command -v docuo &> /dev/null; then
        echo -e "${GREEN}✓ Docuo CLI 安装成功${NC}"
    else
        echo -e "${RED}✗ Docuo CLI 安装失败${NC}"
        echo -e "${YELLOW}请尝试手动安装: npm install -g @spreading/docuo${NC}"
    fi
fi

echo ""

# 3. 将.hooks下的脚本都复制到.git/hooks下
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

# 6. 启动开发服务器
echo -e "${YELLOW}6. 启动开发服务器${NC}"
echo -e "${BLUE}环境设置完成！现在可以启动开发服务器:${NC}"
echo -e "${GREEN}docuo dev${NC}"
echo ""
echo -e "${YELLOW}提示:${NC}"
echo -e "• 首次运行后，可以使用 ${GREEN}docuo dev --noinstall${NC} 加快启动速度"
echo -e "• 如果遇到问题，可以运行: ${GREEN}docuo clear && docuo dev${NC}"
echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}    环境设置完成！${NC}"
echo -e "${BLUE}========================================${NC}" 