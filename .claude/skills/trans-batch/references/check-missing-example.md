# 查漏补缺功能使用指南

## 概述

`check_missing_translations.py` 脚本用于扫描英文实例的 `sidebars.json` 文件，找出所有未翻译的文档（即 label 仍包含中文的文档）。

## 工作原理

1. 读取英文实例目录下的 `sidebars.json`
2. 遍历所有 `type="doc"` 的节点
3. 检查节点的 `label` 是否包含中文字符
4. 如果包含中文，说明该文档未翻译
5. 根据 DOCUO 文档 ID 规则计算对应的 MDX 文件路径
6. 输出待翻译文件列表

## 文档 ID 转换规则

DOCUO 的文档 ID 转换规则（详见 [DOCUO_CONFIG_GUIDE.md](../../DOCUO_CONFIG_GUIDE.md)）：

1. **相对路径**：文档 ID 相对于实例目录
2. **无扩展名**：`.mdx` 扩展名不包含在 ID 中
3. **小写 + 连字符**：空格和下划线变为连字符
4. **移除数字前缀**：`01-`、`02-` 前缀被移除

**转换示例**：

| 原始路径/ID | 转换后的文档 ID |
|------------|----------------|
| `Quick Start/Setup.mdx` | `quick-start/setup` |
| `01-Introduction/02-Overview.mdx` | `introduction/overview` |

脚本使用反向查找策略：
1. 尝试直接匹配 `doc_id.mdx`
2. 尝试带数字前缀 `01-doc_id.mdx`, `02-doc_id.mdx`
3. 尝试在子目录中查找（处理 doc_id 包含 `/` 的情况）

## 使用示例

### 示例 1：检查单个实例（默认 JSON 输出）

```bash
python3 .claude/skills/trans-batch/scripts/check_missing_translations.py \
  core_products/real-time-voice-video/en/android-java
```

**JSON 输出**（默认格式）：
```json
{
  "summary": {
    "total": 14,
    "existing": 14,
    "missing": 0
  },
  "files": [
    {
      "doc_id": "client-sdk/api-reference/function-list",
      "label": "功能总览",
      "mdx_path": "core_products/real-time-voice-video/en/android-java/client-sdk/api-reference/function-list.mdx",
      "sidebar_path": "core_products/real-time-voice-video/en/android-java/sidebars.json",
      "exists": true,
      "path_in_sidebar": "clientApi"
    },
    {
      "doc_id": "introduction/entry",
      "label": "实时音视频",
      "mdx_path": "core_products/real-time-voice-video/en/android-java/introduction/entry.mdx",
      "sidebar_path": "core_products/real-time-voice-video/en/android-java/sidebars.json",
      "exists": true,
      "path_in_sidebar": "mySidebar > Introduction"
    }
  ]
}
```

### 示例 2：人类可读的文本输出

```bash
python3 .claude/skills/trans-batch/scripts/check_missing_translations.py \
  core_products/real-time-voice-video/en/android-java --text
```

**文本输出**：
```
Scanning instance: core_products/real-time-voice-video/en/android-java

Found 14 untranslated documents:

Summary:
  - Total untranslated: 14
  - Files exist (can be translated): 14
  - Files missing (need investigation): 0

================================================================================
Untranslated documents:
================================================================================

1. [✓] 功能总览
   Doc ID: client-sdk/api-reference/function-list
   MDX Path: core_products/real-time-voice-video/en/android-java/client-sdk/api-reference/function-list.mdx
   Sidebar Path: clientApi

2. [✓] 实时音视频
   Doc ID: introduction/entry
   MDX Path: core_products/real-time-voice-video/en/android-java/introduction/entry.mdx
   Sidebar Path: mySidebar > Introduction

...
```

### 示例 3：检查整个英文目录（多个实例）

```bash
python3 .claude/skills/trans-batch/scripts/check_missing_translations.py \
  core_products/real-time-voice-video/en
```

这会扫描 `/en/` 目录下的所有实例（android-java, ios-oc, flutter 等）。

### 示例 4：使用 jq 提取特定字段

```bash
# 提取所有 MDX 文件路径
python3 .claude/skills/trans-batch/scripts/check_missing_translations.py \
  core_products/real-time-voice-video/en/android-java | jq -r '.files[].mdx_path'

# 提取 doc_id 和 label
python3 .claude/skills/trans-batch/scripts/check_missing_translations.py \
  core_products/real-time-voice-video/en/android-java | jq '.files[] | {doc_id, label}'

# 只获取统计摘要
python3 .claude/skills/trans-batch/scripts/check_missing_translations.py \
  core_products/real-time-voice-video/en/android-java | jq '.summary'
```

**输出格式说明**：
- **默认输出**：纯 JSON 格式（方便程序读取和管道处理）
- **--text 标志**：人类可读的文本格式（适合直接查看）
- **JSON 结构**：
  - `summary.total`: 未翻译文档总数
  - `summary.existing`: 文件存在的数量（可翻译）
  - `summary.missing`: 文件缺失的数量（需调查）
  - `files[]`: 每个未翻译文档的详细信息

## 使用场景

### 场景 1：批量翻译后的完整性检查

在完成批量翻译后，运行脚本检查是否有遗漏：

```bash
python3 .claude/skills/trans-batch/scripts/check_missing_translations.py \
  core_products/real-time-voice-video/en

# 如果输出 "All documents are translated!"，说明翻译完成
# 如果列出未翻译文档，继续翻译这些文件
```

### 场景 2：部分翻译失败重试

翻译过程中某些文件可能失败（如超时、网络问题），使用脚本找出这些文件：

```bash
python3 .claude/skills/trans-batch/scripts/check_missing_translations.py \
  core_products/real-time-voice-video/en/android-java > failed_files.json

# 查看 failed_files.json，重新翻译这些文件
```

### 场景 3：翻译进度验证

定期检查翻译进度：

```bash
# 在翻译初期（使用 jq 获取统计）
python3 .claude/skills/trans-batch/scripts/check_missing_translations.py \
  core_products/real-time-voice-video/en | jq '.summary'
# {"total": 150, "existing": 150, "missing": 0}

# 在翻译中期
python3 .claude/skills/trans-batch/scripts/check_missing_translations.py \
  core_products/real-time-voice-video/en | jq '.summary'
# {"total": 75, "existing": 75, "missing": 0}

# 在翻译后期
python3 .claude/skills/trans-batch/scripts/check_missing_translations.py \
  core_products/real-time-voice-video/en | jq '.summary'
# {"total": 10, "existing": 10, "missing": 0}

# 翻译完成
python3 .claude/skills/trans-batch/scripts/check_missing_translations.py \
  core_products/real-time-voice-video/en | jq '.summary.total'
# 0（或未翻译文档列表为空）
```

## 与批量翻译流程集成

查漏补缺可以与现有的批量翻译流程无缝集成：

### 方式 1：翻译前检查

```bash
# 0.1 检查当前翻译状态
python3 .claude/skills/trans-batch/scripts/check_missing_translations.py \
  core_products/real-time-voice-video/en

# 0.2 如果发现有未翻译文档，继续正常流程
python3 .claude/skills/trans-batch/scripts/scan_batch_translation.py \
  core_products/real-time-voice-video/zh/flutter > scan_result.json
```

### 方式 2：翻译后验证

```bash
# 5. 完成所有批次翻译后
python3 .claude/skills/trans-batch/scripts/progress_manager.py show <目标目录>

# 6. 使用查漏补缺验证完整性
python3 .claude/skills/trans-batch/scripts/check_missing_translations.py \
  core_products/real-time-voice-video/en
```

### 方式 3：针对遗漏文档的翻译

如果查漏补缺发现遗漏文档，可以：

1. 保存遗漏文档列表到 JSON 文件
2. 使用 jq 提取这些文档的路径
3. 创建新的翻译任务，只翻译这些文件

```bash
# 1. 查找遗漏文档（默认 JSON 输出）
python3 .claude/skills/trans-batch/scripts/check_missing_translations.py \
  core_products/real-time-voice-video/en/android-java > missing.json

# 2. 提取文档路径（使用 jq）
cat missing.json | jq -r '.files[].mdx_path' > files_to_translate.txt

# 3. 或者直接管道处理（无需保存中间文件）
python3 .claude/skills/trans-batch/scripts/check_missing_translations.py \
  core_products/real-time-voice-video/en/android-java | \
  jq -r '.files[].mdx_path' > files_to_translate.txt

# 4. 查看待翻译文件列表
cat files_to_translate.txt

# 5. 逐个翻译这些文件（或批量处理）
while read -r file; do
  echo "Translating: $file"
  # 执行翻译操作（如调用翻译 API 或手动翻译）
done < files_to_translate.txt
```

## 输出说明

### 统计信息

- **Total untranslated**: 未翻译文档总数
- **Files exist (can be translated)**: MDX 文件存在，可以直接翻译
- **Files missing (need investigation)**: MDX 文件不存在，需要检查

### 文件状态标识

- **[✓]**: 文件存在，可以翻译
- **[✗]**: 文件不存在，需要调查原因

### 常见问题

**Q: 为什么 MDX 文件不存在？**

A: 可能原因：
1. 文件路径配置错误（sidebars.json 中的 doc_id 不正确）
2. 文件被移动或删除
3. 数字前缀命名不匹配

**Q: 如何处理文件缺失的情况？**

A: 检查 sidebars.json 中的 doc_id 是否正确，或者手动查找文件位置。

**Q: 脚本能否自动修复文件路径？**

A: 不能。脚本只负责检测和报告，修复需要手动处理。

## 技术细节

### 中文字符检测

使用 Unicode 范围检测：
```python
def has_chinese(text: str) -> bool:
    return any('\u4e00' <= ch <= '\u9fff' for ch in text)
```

### 递归遍历侧边栏

脚本递归遍历 `sidebars.json` 中的所有节点：
- `type: "doc"` - 文档节点
- `type: "category"` - 分类节点（继续遍历子项）
- `type: "link"` - 链接节点（跳过）

### 智能文件匹配

由于 DOCUO 会规范化文档 ID（移除数字前缀、转小写等），脚本使用多种策略查找原始文件：
1. 直接匹配（doc_id.mdx）
2. 带数字前缀匹配（01-doc_id.mdx）
3. 子目录递归查找
