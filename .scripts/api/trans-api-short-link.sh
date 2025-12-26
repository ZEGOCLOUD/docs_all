#!/bin/bash

# 转换 API 短链接脚本
# 用法: ./.scripts/api/trans-api-short-link.sh

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 切换到项目根目录
cd "$SCRIPT_DIR/../.." || exit 1

# 运行 Node.js 脚本
node .scripts/api/trans-api-short-link/init.mjs "$@"
