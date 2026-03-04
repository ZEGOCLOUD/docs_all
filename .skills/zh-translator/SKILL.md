---
name: zh-translator
description: 中文文档翻译助手。用于将中文文档翻译成英文，支持 Markdown 文档和 OpenAPI YAML 文件。基于 git commit 历史分析改动或指定目录扫描，使用术语一致性对照表。当用户需要翻译中文文档、OpenAPI 配置、指定 commit 范围翻译时使用此 skill。
---

# 中文文档翻译助手

## 概述

本 Skill 提供系统化的中文到英文翻译工作流，支持两种文件类型：
- **Markdown 文档翻译**：基于 git commit 历史分析改动
- **OpenAPI YAML 翻译**：指定目录扫描并翻译

核心功能：
- 生成待翻译任务列表并与用户确认
- **必须使用术语对照表保持翻译一致性（每次翻译前都要重新加载）**
- 支持多种产品线的专业术语
- 手动翻译确保质量，禁止使用自动化翻译工具
- **自动跳过 `docType: API` 的自动生成文件**

## 使用场景

当用户需要翻译修改过的 Markdown 文档、OpenAPI YAML 配置、指定 commit 范围翻译、批量翻译目录下所有文件（新产品批量翻译）时使用。

## ⚠️ 核心规则（必须遵守）

### 1. 术语对照表使用规则

**✅ 每次翻译前必须重新加载术语对照表**，不能依赖记忆或缓存。

**加载时机**：开始翻译每个文件前、开始翻译每个批次前、切换产品线时、用户明确要求时。

**按顺序加载**（后者覆盖前者）：
1. **通用术语表**：`.translate/common-terminology.csv`
2. **产品术语表(按需)**：`.translate/products/<产品ID>.csv`

**产品识别映射**：
- `real_time_video` / `real_time_voice` → `real_time_video_zh.csv`
- `zim` / `imkit` → `zim_zh.csv`
- `callkit` → `callkit_zh.csv`
- `live_streaming_kit` / `live_audio_room_kit` → `live_streaming_kit_zh.csv`
- `super_board` → `super_board_zh.csv`
- `ai_effects` → `ai_effects_zh.csv`

**强制使用**：
- 所有术语表中的条目必须严格按翻译
- 品牌名必须准确翻译（如 `ZEGO` → `ZEGOCLOUD`）
- 不得随意更改或创造新翻译
- 遇到术语表中没有的新术语，记录下来并建议添加

**常见术语**：
```
ZEGO → ZEGOCLOUD
ZEGO 控制台 → ZEGOCLOUD Console
实时音视频 → Video Call
超低延迟直播 → Live Streaming
拉流 → Play stream
推流 → Publish stream
```

### 2. 自动生成文件识别规则

**必须跳过的文件类型**：

1. **API 文档**：frontmatter 中包含 `docType: API`
   - 识别方法：读取文件前几行，检查是否有 `docType: API`
   - 这类文件是自动生成的，**不需要翻译**

2. **API 文件对**（server 平台）：
   - 同名的 `.mdx` 和 `.yaml` 文件
   - 仅翻译 `.yaml`，跳过 `.mdx`（自动生成）

3. **空文件或仅包含 import 的文件**：
   - 仅更新引用路径（`/zh/` → `/en/`）

### 3. 翻译质量规则（所有文件类型通用）

#### 📋 翻译前准备
- ✅ **必须先阅读术语对照表**，了解专业术语的标准翻译
- ✅ **核心技术概念以参考翻译为准**，保持一致性
- ✅ **必须完整翻译每个文件**，避免翻译一部分就停止

#### 🔤 标点符号处理
- ✅ 所有中文标点符号转为英文标点符号
  - `。` → `.`，`，` → `,`，`；` → `;`，`：` → `:`，`（）` → `()`
  - `《》` → `""` 或斜体
- ✅ **YAML 特殊规则**：如果描述是单行且包含中文冒号 `：`，必须改为多行描述（使用 `|`）

```yaml
# 正确翻译
description: |
  Interface name: Get user list
```

#### ⚠️ 转义字符处理
- ✅ **保留原有的反斜杠转义符**，不要删除
- ✅ 翻译后如果造成 JSX/MDX 语法错误，**必须添加转义符**
  - `<` → `\<`，`>` → `\>`，`{` → `\{`，`}` → `\}`，`:` → `\:` (在特定位置)

#### 📝 内容准确性
- ✅ **忠于原文**，禁止随意扩写或捏造内容
- ✅ **链接地址**可以按中英文实际情况调整
- ✅ **内部链接名称**优先使用 `sidebars.json` 中定义的 label
- ✅ **翻译结果不能出现中文和中文标点符号**，杜绝中英混杂

#### 🚫 内容保持不变
- ❌ **代码块**：代码保持原样不翻译，注释要翻译
- ❌ **URL**：保持原样
- ❌ **API 端点**：保持原样
- ❌ **技术标识符**：保持原样
- ❌ **参数名**：保持原样
- ❌ **Frontmatter 键**：翻译值但保持键名不变
- ❌ **OpenAPI 关键字**：禁止翻译 `info`, `paths`, `get`, `post`, `parameters`, `responses`, `schema` 等

#### ✏️ 格式保持
- ✅ 保留所有 markdown 语法
- ✅ 保留表格结构，翻译单元格内容
- ✅ 保留粗体、斜体、链接等格式
- ✅ 在英文单词和标点之间添加空格
- ✅ 保留 YAML 结构和缩进

### 4. 进度报告与记录

#### 进度报告格式

**每个文件/段落翻译完成后报告：**
```
✅ 已翻译：path/to/source.md → path/to/target.md
```

**批次完成后的报告：**
```
✅ 批次 1/Z 翻译完成
详细进度：
  ✅ file1.md → file1.md (123 行)
  ✅ file2.yaml → file2.yaml (67 行)

本批次统计：
- 翻译文件数：X
- 翻译行数：Y
- 使用术语表：common, <产品名>

当前总进度：
- 已完成批次：1/Z
- 已翻译文件：X/Y
- 已翻译行数：A/B

是否继续翻译下一批？（批次 2/Z）
```

⚠️ **每批完成后必须暂停并等待用户确认**

#### 批次进度记录（必做）

**记录位置**：在目标目录下创建 `.translation-progress.json` 文件

**记录内容**：
```json
{
  "directory": "core_products/real-time-voice-video/zh/android-java",
  "target_directory": "core_products/real-time-voice-video/en/android-java",
  "started_at": "2025-01-02T10:00:00Z",
  "last_updated": "2025-01-02T14:30:00Z",
  "total_batches": 95,
  "completed_batches": 5,
  "total_files": 203,
  "translated_files": 23,
  "total_lines": 38300,
  "translated_lines": 4320,
  "current_batch": 5,
  "status": "in_progress",
  "completed_files": [
    {
      "source": "core_products/real-time-voice-video/zh/android-java/file1.mdx",
      "target": "core_products/real-time-voice-video/en/android-java/file1.mdx",
      "lines": 123,
      "batch": 1,
      "completed_at": "2025-01-02T10:15:00Z"
    }
  ],
  "skipped_files": [
    {
      "path": "core_products/real-time-voice-video/zh/android-java/api/file.mdx",
      "reason": "docType: API",
      "lines": 1050
    },
    {
      "path": "core_products/real-time-voice-video/zh/android-java/api/file.mdx",
      "reason": "mdx_yaml_pair",
      "paired_yaml": "core_products/real-time-voice-video/zh/android-java/api/file.yaml"
    }
  ],
  "failed_files": [],
  "batches": [
    {
      "batch_number": 1,
      "status": "completed",
      "file_count": 21,
      "lines": 697,
      "started_at": "2025-01-02T10:00:00Z",
      "completed_at": "2025-01-02T10:15:00Z"
    }
  ]
}
```

**记录时机**：
- ✅ 开始翻译前：初始化记录文件
- ✅ 每个批次完成后：更新进度
- ✅ 每个文件翻译完成后：记录文件状态
- ✅ 遇到错误时：记录到 `failed_files`
- ✅ 全部完成后：标记 `status: "completed"`

**恢复翻译**：
如果翻译任务意外终止，可以根据 `.translation-progress.json` 恢复：
1. 读取进度文件
2. 跳过已完成的批次和文件
3. 从 `current_batch` 继续翻译

---

## 翻译工作流程

### 场景 1：翻译修改过的 Markdown 文档（基于 commit）

**使用脚本**：`analyze_changes.py`

```bash
# 最新一个提交
python3 .scripts/analyze_changes.py .

# 指定提交到 HEAD
python3 .scripts/analyze_changes.py . abc123

# 提交范围
python3 .scripts/analyze_changes.py . abc123 def456
```

**流程**：
1. 收集待翻译文件，向用户展示并等待确认
2. 逐个文件翻译
   - 确定目标文件路径（`docs/zh/` → `docs/en/`）
   - 加载术语对照表（通用 + 产品特定）
   - 如果目标英文文件不存在，创建新文件并翻译全部内容
   - 如果目标英文文件已存在，分析 git diff，翻译变更内容并插入对应位置
3. 每个文件翻译完成后报告进度

### 场景 2：翻译 OpenAPI YAML（指定目录）

**流程**：
1. 扫描指定目录下所有 `.yaml` 文件
2. 按文件大小排序（小文件优先）
3. 向用户展示并等待确认
4. 分段翻译（< 100 行直接翻译；≥ 100 行分段，每段不超过 2000 行）
5. 只翻译 `description`, `summary`, `example` 等描述性字段的值

**特殊规则**：
- 如果描述是单行且包含中文冒号 `：`，必须改为多行描述（使用 `|`）
- 保留 YAML 结构和缩进，保持键名不变

### 场景 3：批量翻译目录下所有文件（新产品）

**使用脚本**：`scan_translation_files.py`

```bash
# 默认批次大小（5000 行/批）
python3 .skills/zh-translator/scripts/scan_translation_files.py docs/zh/product

# 自定义批次大小
python3 .skills/zh-translator/scripts/scan_translation_files.py docs/zh/product 3000
```

**输出内容**：
1. **统计摘要**：API 文件数量、Markdown 文件数量和行数、YAML 文件数量和行数、总批次、大文件列表（>500 行）
2. **批次计划**：每批包含的文件列表、每批的总行数和文件数、大文件标记
3. **智能识别**：自动识别 API 文件对（mdx + yaml），仅翻译 `.yaml`

**流程**：
1. 扫描目录并生成翻译计划
2. 向用户展示扫描结果并等待确认
3. **初始化进度记录文件**：在目标目录创建 `.translation-progress.json`
4. 逐批次翻译
   - **小文件**（< 100 行）：多个文件一批
   - **中等文件**（100-500 行）：1-2 个文件一批
   - **大文件**（> 500 行）：单独成批，分段翻译（每段不超过 2000 行）
5. **每批次完成后**：
   - 更新 `.translation-progress.json` 文件
   - 报告进度并暂停，等待用户确认
6. 全部完成后提供总结报告，标记 `status: "completed"`

**大文件分段翻译示例**：
```
⚠️ 处理大文件：path/to/large_file.md (2500 行)
📍 第 1/2 段（第 1-1250 行）
[翻译第 1 段...]

✅ 第 1 段完成
📍 第 2/2 段（第 1251-2500 行）
[翻译第 2 段...]

✅ 大文件翻译完成：path/to/large_file.md
```

---

## 重要说明

### ⚠️ 禁止事项

**严格禁止**以下行为：
- ❌ 创建翻译脚本自动翻译
- ❌ 调用第三方翻译 API
- ❌ 使用任何自动化翻译工具
- ❌ 批量生成翻译内容

**必须手动翻译每个文件**，确保翻译质量和准确性。

### ✅ 允许事项

**可以使用脚本**：
- ✅ 分析 git 变更内容（如 `analyze_changes.py`）
- ✅ 扫描目录生成文件列表
- ✅ 加载和查询术语对照表
- ✅ 文件路径转换和定位
- ✅ 差异对比和内容定位

**核心原则**：脚本用于辅助分析和定位，实际翻译必须由 AI 手动完成。

---

## 资源文件

### scripts/
- **analyze_changes.py**：Git 变更分析脚本，用于识别改动的 markdown 文件
- **scan_translation_files.py**：目录扫描脚本，用于批量翻译场景

### .translate/
**术语对照表（维护在项目根目录的 `.translate/` 下）：**
- `common-terminology.csv`：通用术语（品牌名、URL、产品名等）
- `products/`：产品特定术语表
  - `real_time_video_zh.csv`：实时音视频
  - `zim_zh.csv`：即时通讯
  - `callkit_zh.csv`：音视频通话 UIKit
  - `live_streaming_kit_zh.csv`：互动直播 UIKit
  - `super_board_zh.csv`：超级白板
  - `ai_effects_zh.csv`：AI 美颜
