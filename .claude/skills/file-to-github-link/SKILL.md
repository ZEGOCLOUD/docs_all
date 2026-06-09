---
name: file-to-github-link
description: >
  This skill should be used when the user asks to "生成 GitHub 链接", "get GitHub link",
  "file to github link", "生成文件链接", "获取源码链接", or needs to convert a local
  file path + line number into a clickable GitHub URL. Also triggers when the user references
  a file and line number and wants a shareable link to that location in the repository.

  Do NOT trigger for general link checking, link fixing, or web URL tasks — this skill is
  specifically for local-to-GitHub path conversion.
version: 1.0.0
---

# File to GitHub Link

将工作区内文件路径转换为 GitHub 可跳转链接，支持行号定位和分支指定。

## 用法

```bash
bash scripts/file-to-github-link.sh [-b <分支>] <相对路径> [<行号>]
```

### 参数说明

| 参数 | 必填 | 说明 |
|------|------|------|
| 相对路径 | 是 | 相对于 workspace 根目录的文件路径 |
| 行号 | 否 | 跳转到指定行，留空则不定位行号 |
| -b 分支 | 否 | 指定 GitHub 分支，默认 `main` |

### 调用示例

```bash
# 默认 main 分支 + 行号
bash scripts/file-to-github-link.sh docs/ai-agent/web/quick-start.mdx 128
# → https://github.com/{owner}/{repo}/blob/main/docs/.../quick-start.mdx?plain=1#L128

# 指定分支
bash scripts/file-to-github-link.sh -b community docs/ai-agent/web/quick-start.mdx 128

# 只要文件链接，不要行号
bash scripts/file-to-github-link.sh docs/ai-agent/web/quick-start.mdx

# 指定分支 + 无行号
bash scripts/file-to-github-link.sh -b community docs/ai-agent/web/quick-start.mdx
```

## 注意事项

- `.md` / `.mdx` 文件自动追加 `?plain=1`（GitHub 需要此参数才能显示源码模式 + 行号高亮）
- 路径相对于 workspace 根目录，不要以 `/` 开头
- 指定非 main 分支时会校验远端是否存在，不存在会输出警告（链接仍会生成）
- 依赖 `git remote get-url origin`，需在 git 仓库内运行
