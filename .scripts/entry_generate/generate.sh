#!/bin/bash

# Entry Generator 启动脚本
# 用于快速生成产品entry文档

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 脚本目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# 显示帮助信息
show_help() {
    echo -e "${BLUE}📚 Entry Generator - 自动生成产品entry文档${NC}"
    echo ""
    echo "用法: $0 [command] [options]"
    echo ""
    echo "命令:"
    echo "  generate              生成所有产品的entry文档"
    echo "  generate <product>    生成指定产品的entry文档"
    echo "  test                  运行测试用例"
    echo "  list                  列出所有可用的产品"
    echo "  help                  显示帮助信息"
    echo ""
    echo "产品类型:"
    echo "  real-time-voice-video      实时音视频"
    echo "  real-time-voice           实时语音"
    echo "  low-latency-live-streaming 超低延迟直播"
    echo ""
    echo "示例:"
    echo "  $0 generate                           # 生成所有entry"
    echo "  $0 generate real-time-voice-video    # 只生成实时音视频的entry"
    echo "  $0 test                              # 运行测试"
    echo "  $0 list                              # 列出所有产品"
}

# 检查Node.js环境
check_node() {
    if ! command -v node &> /dev/null; then
        echo -e "${RED}❌ Node.js not found. Please install Node.js first.${NC}"
        exit 1
    fi
    
    local node_version=$(node --version | cut -d'v' -f2 | cut -d'.' -f1)
    if [ "$node_version" -lt 12 ]; then
        echo -e "${YELLOW}⚠️  Node.js version is too old. Recommended: v12 or higher${NC}"
    fi
}

# 切换到项目根目录
cd_to_project_root() {
    cd "$PROJECT_ROOT"
    echo -e "${BLUE}📁 Working directory: $(pwd)${NC}"
}

# 运行生成器
run_generator() {
    echo -e "${GREEN}🚀 Starting entry generation...${NC}"
    echo ""
    
    cd "$SCRIPT_DIR"
    
    if [ $# -eq 0 ]; then
        node index.js generate
    else
        node index.js generate "$1"
    fi
}

# 运行测试
run_tests() {
    echo -e "${GREEN}🧪 Running tests...${NC}"
    echo ""
    
    cd "$SCRIPT_DIR"
    node test.js test
}

# 列出产品
list_products() {
    echo -e "${GREEN}📋 Listing products...${NC}"
    echo ""
    
    cd "$SCRIPT_DIR"
    node index.js list
}

# 主程序
main() {
    # 检查环境
    check_node
    cd_to_project_root
    
    # 解析命令
    case "${1:-generate}" in
        "generate")
            if [ -n "$2" ]; then
                run_generator "$2"
            else
                run_generator
            fi
            ;;
        "test")
            run_tests
            ;;
        "list")
            list_products
            ;;
        "help"|"--help"|"-h")
            show_help
            ;;
        *)
            echo -e "${RED}❌ Unknown command: $1${NC}"
            echo ""
            show_help
            exit 1
            ;;
    esac
}

# 执行主程序
main "$@"
