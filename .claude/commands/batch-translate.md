---
name: batch-translate
description: 批量翻译文档的交互式命令。收集指定产品或目录下的待翻译文件，然后使用 batch-translator agent 进行批量翻译。触发词：批量翻译、batch translate、翻译产品文档。
trigger: batch-translate
---

# Batch Translate Command

批量翻译指定产品或目录下的待翻译文档。

## 执行流程

1. **确定翻译目标** - 获取用户指定的产品/目录
2. **收集待翻译文件** - 使用 collect-pending-translation-files skill 扫描
3. **执行批量翻译** - 调用 batch-translator agent 完成翻译

---

## Step 1: 确定翻译目标

如果命令参数 `$ARGUMENTS` 为空，请询问用户：

**常用产品路径：**
| 产品名称 | 中文路径 | 英文路径 |
|---------|---------|---------|
| AIAgent | `core_products/aiagent/zh` | `core_products/aiagent/en` |
| 实时音视频 | `core_products/real-time-voice-video/zh` | `core_products/real-time-voice-video/en` |
| 直播 | `core_products/live-streaming/zh` | `core_products/live-streaming/en` |
| ZIM | `core_products/zim/zh` | `core_products/zim/en` |
| Call Kit | `uikit_kits/call-kit/zh` | `uikit_kits/call-kit/en` |
| Live Audio Room Kit | `uikit_kits/live-audio-room-kit/zh` | `uikit_kits/live-audio-room-kit/en` |

**支持的输入格式：**
- 产品名称：如 `aiagent`、`AIAgent`、`实时音视频`
- 完整路径：如 `core_products/aiagent/zh` 或 `core_products/aiagent/en`
- 平台路径：如 `core_products/aiagent/zh/flutter`（只翻译 Flutter 平台）

当前参数：`$ARGUMENTS`

## Step 2: 收集待翻译文件

使用 collect-pending-translation-files skill 扫描目标目录，生成待翻译文件列表。

<skill>
skill: collect-pending-translation-files
args: $ARGUMENTS
</skill>

## Step 3: 执行批量翻译

调用 batch-translator agent 开始批量翻译。

<agent>
description: batch-translator
prompt: 执行批量翻译任务。

目标目录：$ARGUMENTS

**任务说明：**
1. 查找最近生成的待翻译文件列表（/tmp/docs-pending-translation-*.json 中最新的文件）
2. 按顺序逐个翻译文件，严格遵循 translate-zh-to-en skill 的规则
3. 每完成一个文件后立即更新进度文件
4. 报告翻译进度和结果

**重要规则：**
- 手动翻译，不使用自动化翻译工具
- 跳过自动生成的 API 文档（frontmatter 有 api 字段）
- 保留 MDX 语法和代码块
- 翻译完成后检查是否还有中文字符

如果存在多个待翻译列表文件，使用时间戳最新的一个。
subagent_type: batch-translator
</agent>

---

**提示**：如果翻译过程中断，可以：
- 再次运行 `/batch-translate` 继续翻译
- 或直接说"继续翻译"让 batch-translator agent 恢复工作
