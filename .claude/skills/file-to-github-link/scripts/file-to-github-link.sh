#!/bin/bash
# 将工作区内文件路径+行号转换为 GitHub 可跳转链接
# 用法: doc-link.sh [-b <分支名>] <相对路径> [<行号>]
# 默认使用 main 分支；可通过 -b 指定远端分支
# 示例:
#   doc-link.sh docs/ai-agent/web/quick-start.mdx 128
#   doc-link.sh -b community docs/ai-agent/web/quick-start.mdx 128
#   doc-link.sh -b community docs/ai-agent/web/quick-start.mdx

set -euo pipefail

# 默认分支
BRANCH="main"

# 解析 -b 参数
while getopts "b:" opt; do
  case "$opt" in
    b) BRANCH="$OPTARG" ;;
    *)
      echo "用法: doc-link.sh [-b <分支名>] <相对路径> [<行号>]" >&2
      exit 1
      ;;
  esac
done
shift $((OPTIND - 1))

if [ $# -lt 1 ]; then
  echo "用法: doc-link.sh [-b <分支名>] <相对路径> [<行号>]" >&2
  exit 1
fi

REL_PATH="$1"
LINE="${2:-}"

# 从 git remote 自动提取 owner/repo
REMOTE_URL=$(git remote get-url origin 2>/dev/null || echo "")
REPO=$(echo "$REMOTE_URL" | sed -E 's|git@github.com:([^/]+/[^/]+)\.git|\1|;s|https://github.com/([^/]+/[^/]+)(\.git)?|\1|')

if [ -z "$REPO" ]; then
  echo "错误: 无法从 git remote 获取仓库地址" >&2
  exit 1
fi

# 如果用户指定了分支，验证远端是否存在
if [ "$BRANCH" != "main" ]; then
  if ! git ls-remote --heads origin "refs/heads/${BRANCH}" 2>/dev/null | grep -q .; then
    echo "警告: 远端不存在分支 '${BRANCH}'，链接可能无法访问" >&2
  fi
fi

URL="https://github.com/${REPO}/blob/${BRANCH}/${REL_PATH}"
# .mdx/.md 文件需要 ?plain=1 才能显示源码并支持行号跳转
case "$REL_PATH" in
  *.md|*.mdx) URL="${URL}?plain=1" ;;
esac
if [ -n "$LINE" ]; then
  URL="${URL}#L${LINE}"
fi

echo "$URL"
