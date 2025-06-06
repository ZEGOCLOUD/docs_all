#!/bin/bash

# AI数据更新脚本启动器

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 项目配置
PYTHON_VERSION="3.8"  # 最低要求版本
VENV_NAME="venv"

# 打印带颜色的消息
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查命令是否存在
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# 检查Python版本
check_python_version() {
    if command_exists python3; then
        PYTHON_CMD="python3"
    elif command_exists python; then
        PYTHON_CMD="python"
    else
        print_error "Python 未安装。请先安装 Python $PYTHON_VERSION 或更高版本。"
        print_info "推荐使用 Homebrew 安装: brew install python"
        exit 1
    fi

    # 检查Python版本
    CURRENT_VERSION=$($PYTHON_CMD -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
    REQUIRED_VERSION_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
    REQUIRED_VERSION_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)
    CURRENT_VERSION_MAJOR=$(echo $CURRENT_VERSION | cut -d. -f1)
    CURRENT_VERSION_MINOR=$(echo $CURRENT_VERSION | cut -d. -f2)

    if [ "$CURRENT_VERSION_MAJOR" -lt "$REQUIRED_VERSION_MAJOR" ] ||
       ([ "$CURRENT_VERSION_MAJOR" -eq "$REQUIRED_VERSION_MAJOR" ] && [ "$CURRENT_VERSION_MINOR" -lt "$REQUIRED_VERSION_MINOR" ]); then
        print_error "Python 版本过低。当前版本: $CURRENT_VERSION，要求版本: $PYTHON_VERSION+"
        exit 1
    fi

    print_success "Python 版本检查通过: $CURRENT_VERSION"
}

# 创建虚拟环境
create_virtual_env() {
    print_info "创建虚拟环境..."

    if [ -d "$VENV_NAME" ]; then
        print_warning "虚拟环境已存在，是否重新创建? (y/N)"
        read -r response
        if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
            print_info "删除现有虚拟环境..."
            rm -rf "$VENV_NAME"
        else
            print_info "使用现有虚拟环境"
            return 0
        fi
    fi

    $PYTHON_CMD -m venv "$VENV_NAME"
    print_success "虚拟环境创建完成: $VENV_NAME"
}

# 安装依赖
install_dependencies() {
    print_info "检查并安装项目依赖..."

    # 定义项目依赖
    DEPENDENCIES=(
        "requests>=2.25.0"
        "crawl4ai"
        "pathlib"
    )

    # 升级pip
    pip install --upgrade pip

    # 安装依赖
    for dep in "${DEPENDENCIES[@]}"; do
        print_info "安装 $dep..."
        pip install "$dep"
    done

    print_success "依赖安装完成"
}

# 验证安装
verify_installation() {
    print_info "验证安装..."

    python -c "
import sys
import requests
try:
    from crawl4ai import AsyncWebCrawler
    print('✅ crawl4ai 导入成功')
except ImportError as e:
    print('❌ crawl4ai 导入失败:', e)
    sys.exit(1)
print('✅ 所有依赖验证通过')
"

    if [ $? -eq 0 ]; then
        print_success "依赖验证通过"
    else
        print_error "依赖验证失败"
        exit 1
    fi
}

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 检查Python版本
check_python_version

# 检查并创建虚拟环境
if [ ! -d "venv" ]; then
    print_info "虚拟环境不存在，开始创建..."
    create_virtual_env
    source venv/bin/activate
    install_dependencies
    verify_installation
else
    source venv/bin/activate
    print_success "虚拟环境已激活"
fi

# 检查必要的依赖
echo "🔍 检查依赖..."
python -c "import requests; print('✅ requests 可用')" 2>/dev/null || {
    echo "❌ requests 未安装，正在安装..."
    pip install requests
}

python -c "import crawl4ai; print('✅ crawl4ai 可用')" 2>/dev/null || {
    echo "⚠️  crawl4ai 未安装，页面下载功能将不可用"
    echo "   如需使用页面下载功能，请运行: pip install crawl4ai"
}

# 检查配置文件
echo "🔍 检查配置文件..."
if [ -f "../../docuo.config.zh.json" ]; then
    echo "✅ 中文配置文件存在"
else
    echo "❌ 中文配置文件不存在: docuo.config.zh.json"
fi

if [ -f "../../docuo.config.en.json" ]; then
    echo "✅ 英文配置文件存在"
else
    echo "❌ 英文配置文件不存在: docuo.config.en.json"
fi

# 检查环境变量
echo "🔍 检查环境变量..."
if [ -z "$RAGFLOW_BASE_URL" ]; then
    echo "⚠️  RAGFLOW_BASE_URL 环境变量未设置"
fi

if [ -z "$RAGFLOW_API_KEY" ]; then
    echo "⚠️  RAGFLOW_API_KEY 环境变量未设置"
fi

# 显示使用说明
echo ""
echo "=== AI数据更新脚本 ==="
echo "本脚本将完整执行：页面下载 -> Dataset更新 -> Assistant更新"
echo ""
echo "使用说明："
echo "1. 脚本会询问处理中文还是英文（默认中文）"
echo "2. 选择要处理的产品组"
echo "3. 选择要处理的实例（可选择全部）"
echo "4. 自动执行完整流程"
echo ""

# 运行AI数据更新脚本
echo "🚀 启动AI数据更新脚本..."
python update_ai_data.py "$@"

# 检查执行结果
if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 AI数据更新脚本执行完成！"
    echo ""
    echo "📁 数据文件位置: .scripts/ai_data/data/"
    echo "🔧 配置文件位置: static/data/ai_search_mapping.json"
    echo ""
else
    echo ""
    echo "❌ 脚本执行过程中发生错误"
    echo ""
    echo "故障排除建议："
    echo "1. 检查网络连接"
    echo "2. 确认环境变量设置正确"
    echo "3. 运行测试脚本: python test_update_ai_data.py"
    echo "4. 查看详细错误信息"
    echo ""
fi
