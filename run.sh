#!/bin/bash

# 设置颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 检查 docuo 是否存在且为最新版本
NPM_REGISTRY="--registry=https://registry.npmmirror.com"
NEED_SETUP=false

if ! command -v docuo &> /dev/null; then
    echo -e "${YELLOW}未检测到 docuo${NC}"
    NEED_SETUP=true
else
    CURRENT_DOCUO_VERSION=$(npm list -g @spreading/docuo --depth=0 2>/dev/null | grep @spreading/docuo | sed 's/.*@spreading\/docuo@//')
    LATEST_DOCUO_VERSION=$(npm view @spreading/docuo version $NPM_REGISTRY 2>/dev/null)
    if [ "$CURRENT_DOCUO_VERSION" != "$LATEST_DOCUO_VERSION" ]; then
        echo -e "${YELLOW}Docuo CLI 版本不是最新 (当前: ${CURRENT_DOCUO_VERSION}, 最新: ${LATEST_DOCUO_VERSION})${NC}"
        NEED_SETUP=true
    fi
fi

if [ "$NEED_SETUP" = true ]; then
    echo -e "${YELLOW}正在执行 setup.sh...${NC}"
    bash "$(dirname "$0")/setup.sh"

    if ! command -v docuo &> /dev/null; then
        echo -e "${RED}✗ 安装失败，请手动执行 setup.sh${NC}"
        exit 1
    fi
fi

# 从 docuo.config.*.json 重新生成 FAQ 维度（幂等）。改了 config 后，下次预览自动同步 FAQ 下拉/instanceMap。
SCRIPT_DIR="$(dirname "$0")"
if [ -f "$SCRIPT_DIR/.scripts/faq/generate_faq_dimensions.mjs" ] && command -v node &> /dev/null; then
    echo -e "${BLUE}正在同步 FAQ 维度（docuo.config.*.json → faqDimensions.js）...${NC}"
    if ! node "$SCRIPT_DIR/.scripts/faq/generate_faq_dimensions.mjs" >/dev/null; then
        echo -e "${YELLOW}⚠ FAQ 维度生成失败，已跳过（不影响启动）。可手动排查：node .scripts/faq/generate_faq_dimensions.mjs${NC}"
    fi
    # 预生成 curl 可取的静态 JSON（每 instance 一个文件 → static/faq-instance/<id>.json）。依赖上面的维度。
    echo -e "${BLUE}正在生成 FAQ 静态数据（static/faq-instance/*.json，供 curl 消费）...${NC}"
    node "$SCRIPT_DIR/.scripts/faq/generate_static_faq.mjs" >/dev/null || echo -e "${YELLOW}⚠ FAQ 静态数据生成失败，已跳过。${NC}"
fi

# 解析命令行参数
case "$1" in
    --zh)
        echo -e "${GREEN}启动中文文档...${NC}"
        docuo dev --zh
        exit 0
        ;;
    --en)
        echo -e "${GREEN}启动英文文档...${NC}"
        docuo dev --en
        exit 0
        ;;
esac

# 交互选择语言（无参数时）
echo -e "${BLUE}请选择文档语言:${NC}"
echo -e "  ${GREEN}1) 中文${NC} (默认)"
echo -e "  ${GREEN}2) 英文${NC}"
read -rp "请输入选择 [1/2]: " LANG_CHOICE

case "$LANG_CHOICE" in
    2)
        echo -e "${GREEN}启动英文文档...${NC}"
        docuo dev --en
        ;;
    *)
        echo -e "${GREEN}启动中文文档...${NC}"
        docuo dev --zh
        ;;
esac

