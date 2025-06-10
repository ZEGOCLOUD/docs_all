#!/bin/bash

# 目录及文件名格式化脚本启动器

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
# import sys
# import requests
# try:
#     from crawl4ai import AsyncWebCrawler
#     print('✅ crawl4ai 导入成功')
# except ImportError as e:
#     print('❌ crawl4ai 导入失败:', e)
#     sys.exit(1)
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



# 运行目录及文件名格式化脚本
echo "🚀 启动目录及文件名格式化脚本..."
python convert.py "$@"

# 检查执行结果
if [ $? -eq 0 ]; then
    print_success "脚本执行完成"
else
    print_error "脚本执行失败"
    exit 1
fi
