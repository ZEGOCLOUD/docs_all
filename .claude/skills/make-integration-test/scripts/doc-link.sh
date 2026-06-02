#!/bin/bash
# 将工作区内文件路径+行号转换为 GitHub 可跳转链接
# 用法: doc-link.sh <相对路径> [<行号>]
# 自动检测 remote URL 和当前分支（本地分支不在远端时找最近的远端父分支）
# 示例:
#   doc-link.sh docs/ai-agent/web/quick-start.mdx 128
#   doc-link.sh docs/ai-agent/web/quick-start.mdx

set -euo pipefail

if [ $# -lt 1 ]; then
  echo "用法: doc-link.sh <相对路径> [<行号>]" >&2
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

# 找到用于 GitHub 链接的分支名
# 1. 当前分支在远端存在 → 直接用
# 2. 有 upstream 设置 → 用 upstream
# 3. 找所有远端分支中与 HEAD 共享最多历史的那个

LOCAL_BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "")

resolve_branch() {
  # 1. 当前分支是否在远端存在
  if git ls-remote --heads origin "refs/heads/${LOCAL_BRANCH}" 2>/dev/null | grep -q .; then
    echo "$LOCAL_BRANCH"
    return
  fi

  # 2. 是否有 upstream
  local upstream
  upstream=$(git rev-parse --abbrev-ref @{upstream} 2>/dev/null || echo "")
  if [ -n "$upstream" ]; then
    # upstream 格式通常是 origin/xxx，去掉 origin/ 前缀
    echo "$upstream" | sed 's|^origin/||'
    return
  fi

  # 3. 遍历远端分支，找 merge-base 离 HEAD 最近的
  local best_branch=""
  local best_ahead=999999

  while IFS= read -r ref; do
    remote_branch=$(echo "$ref" | sed 's|.*refs/heads/||')
    mb=$(git merge-base HEAD "$ref" 2>/dev/null || echo "")
    [ -z "$mb" ] && continue
    # HEAD 领先 merge-base 的提交数，越小 = 越接近
    ahead=$(git rev-list --count "${mb}..HEAD" 2>/dev/null || echo "999999")
    if [ "$ahead" -lt "$best_ahead" ]; then
      best_ahead="$ahead"
      best_branch="$remote_branch"
    fi
  done < <(git ls-remote --heads origin 2>/dev/null)

  if [ -n "$best_branch" ]; then
    echo "$best_branch"
    return
  fi

  # 兜底
  echo "main"
}

BRANCH=$(resolve_branch)

URL="https://github.com/${REPO}/blob/${BRANCH}/${REL_PATH}"
# .mdx/.md 文件需要 ?plain=1 才能显示源码并支持行号跳转
case "$REL_PATH" in
  *.md|*.mdx) URL="${URL}?plain=1" ;;
esac
if [ -n "$LINE" ]; then
  URL="${URL}#L${LINE}"
fi

echo "$URL"
