#!/bin/bash

# Git push to PR user's remote
# 将当前 pr/* 分支的更改推送到 PR 作者的远程分支

show_help() {
  echo "用法: ./push_to_pr.sh [选项]"
  echo ""
  echo "将当前 pr/* 分支的更改推送到 PR 作者的远程分支"
  echo ""
  echo "选项:"
  echo "  -h, --help    显示此帮助信息"
  echo ""
  echo "示例:"
  echo "  ./push_to_pr.sh           # 交互式选择目标分支（默认 main）"
  echo ""
  echo "注意: 必须在 pr/username/number 格式的分支上执行此脚本"
}

# 处理命令行参数
if [[ "$1" == "-h" || "$1" == "--help" ]]; then
  show_help
  exit 0
fi

# 获取当前分支
current_branch=$(git branch --show-current)

# 检查是否在 pr/* 分支
if [[ $current_branch != pr/* ]]; then
  echo "错误: 当前分支不是 pr/* 格式"
  echo "当前分支: $current_branch"
  exit 1
fi

# 提取用户名（pr/username/number 中的 username）
username=$(echo "$current_branch" | cut -d'/' -f2)

# 交互式询问目标分支
echo "当前分支: $current_branch"
echo "PR 作者: $username"
echo ""
read -p "请输入目标分支名 [main]: " target_branch

# 如果用户直接回车，使用默认值 main
target_branch=${target_branch:-main}

# 构建并执行推送命令
push_cmd="git push $username HEAD:$target_branch"
echo ""
echo "执行命令: $push_cmd"
eval "$push_cmd"

