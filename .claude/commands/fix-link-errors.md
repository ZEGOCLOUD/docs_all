---
name: fix-link-errors
description: 检查并修复MDX文档中的链接错误。运行链接检查后自动修复错误。
trigger: fix-link-errors
---

# Fix Link Errors

这个命令会检查并修复MDX文档中的链接错误。

## 执行流程

1. **获取检查范围** - 您输入产品平台、或实例ID、或目录路径
2. **运行链接检查** - 使用check-links-in-mdx skill检查链接
3. **修复链接错误** - 使用link-fixer agent修复错误

## Step 1: 获取检查范围

请输入以下任一格式的内容：

- **产品+平台+语言**：如 `实时音视频 iOS OC 英文` 或 `aiagent Android 中文`
- **实例ID+语言**：如 `real_time_video_ios_oc_zh` 或 `aiagent_android_zh`
- **完整目录路径**：如 `core_products/aiagent/zh/`

<input>
请输入您要检查的文档范围：
</input>

## Step 2: 运行链接检查

根据您的输入，运行链接检查脚本。

<skill>
skill: check-links-in-mdx
args: {user_input}
</skill>

链接检查已完成，结果保存到 `.scripts/check/check_link_result.json`。

## Step 3: 修复链接错误

现在使用 link-fixer agent 处理修复工作。

<agent>
description: link-fixer
prompt: 读取 .scripts/check/check_link_result.json 文件中的链接检查结果，然后使用 fix-internal-link-error 和 fix-link-anchor-error skills 来修复所有链接错误。

请：
1. 读取并解析 check_link_result.json
2. 按错误类型分组（内部链接错误、锚点错误）
3. 并发调用相应的skills进行修复
4. 报告修复结果摘要

如果结果文件不存在或为空，请报告。
subagent_type: link-fixer
</agent>

## 完成

链接检查和修复工作已完成！