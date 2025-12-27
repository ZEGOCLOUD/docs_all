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
- 使用术语对照表保持翻译一致性
- 支持多种产品线的专业术语
- 手动翻译确保质量，禁止使用自动化翻译工具

## 使用场景

当用户需要：
- 翻译修改过的 Markdown 文档到英文
- 翻译 OpenAPI YAML 配置文件
- 指定 commit hash 或范围进行批量翻译
- **翻译指定目录下的所有文件（新产品批量翻译）**
- 保持术语翻译的一致性
- 自动识别文件对应的产品线
- 分批次翻译大量文件，逐批确认

## 翻译工作流程

### 步骤 1：识别翻译类型

首先确定用户要翻译的文件类型：

**翻译修改过的 Markdown 文档？** → 跳转到「Markdown 文档翻译工作流」
**翻译 OpenAPI YAML（指定目录）？** → 跳转到「OpenAPI YAML 翻译工作流」
**批量翻译目录下所有文件（新产品）？** → 跳转到「批量文件翻译工作流」

---

## Markdown 文档翻译工作流

### 步骤 1：收集待翻译文件

使用 `analyze_changes.py` 脚本分析 git 提交历史：

**使用方法：**
```bash
python3 .scripts/analyze_changes.py <仓库路径> [起始commit] [结束commit]
```

**示例：**
- 最新一个提交：`python3 .scripts/analyze_changes.py .`
- 指定提交到 HEAD：`python3 .scripts/analyze_changes.py . abc123`
- 提交范围：`python3 .scripts/analyze_changes.py . abc123 def456`

**输出：** JSON 格式的改动文件列表及统计信息

**向用户展示：**
```
找到 X 个需要翻译的文件（从 <起始>..<结束>）：

1. path/to/file1.md ( +123 行, -45 行)
2. path/to/file2.md ( +67 行, -12 行)
...

是否开始翻译这些文件？(请确认)
```

⚠️ **必须等待用户明确确认后再继续**

### 步骤 2：逐个文件翻译

#### 2.1 特殊文件处理

**重要规则：**
- 对于 `server` 平台下 `api-reference` 目录下存在同名 `.mdx` 和 `.yaml` 后缀的文件
- **只翻译 `.yaml` 文件**
- `.mdx` 文件是由脚本根据 `.yaml` 自动生成的，无需手动翻译

#### 2.2 确定目标文件路径

根据文件路径模式确定英文文件位置：
- 中文文件：`docs/zh/product/feature.md`
- 英文文件：`docs/en/product/feature.md`

#### 2.3 加载术语对照表

**按顺序加载**（后者覆盖前者）：

1. **通用术语表**：`.translate/common-terminology.csv`
2. **产品术语表(按需)**：`.translate/products/<产品ID>.csv`

**产品识别映射：**
根据文件路径中的关键词识别产品：
- `real_time_video` → `real_time_video_zh.csv`
- `real_time_voice` → `real_time_video_zh.csv`（共用视频术语表）
- `zim` → `zim_zh.csv`
- `callkit` → `callkit_zh.csv`
- `live_streaming_kit` → `live_streaming_kit_zh.csv`
- `live_audio_room_kit` → `live_streaming_kit_zh.csv`（共用直播术语表）
- `imkit` → `zim_zh.csv`（共用 ZIM 术语表）
- `super_board` → `super_board_zh.csv`
- `ai_effects` → `ai_effects_zh.csv`

#### 2.4 翻译策略

**情况 A：目标英文文件不存在**
- 创建新的英文文件
- 翻译整个中文文件内容
- 保持原有的 markdown 结构和格式

**情况 B：目标英文文件已存在**
- 分析 git diff 找出变更的内容
- 根据上下文或关键字定位到英文文档的对应位置
- 将变更内容翻译后插入对应位置
- 保持周围内容的连贯性

### 步骤 3：Markdown 翻译执行

**必须遵守的规则：**

#### 📋 翻译前准备
- ✅ **必须先阅读术语对照表**，了解专业术语的标准翻译
- ✅ **核心技术概念以参考翻译为准**，保持一致性

#### 🔤 标点符号处理
- ✅ 所有中文标点符号转为英文标点符号
  - `。` → `.`
  - `，` → `,`
  - `；` → `;`
  - `：` → `:`
  - `（）` → `()`
  - `《》` → `""` 或斜体

#### ⚠️ 转义字符处理
- ✅ **保留原有的反斜杠转义符**，不要删除
- ✅ 翻译后如果造成 JSX/MDX 语法错误，**必须添加转义符**
  - `<` → `\<`
  - `>` → `\>`
  - `{` → `\{`
  - `}` → `\}`
  - `:` → `\:` (在特定位置)

#### 📝 内容准确性
- ✅ **忠于原文**，禁止随意扩写或捏造内容
- ✅ **链接地址**可以按中英文实际情况调整
- ✅ **内部链接名称**优先使用 `sidebars.json` 中定义的 label
- ✅ **必须完整翻译每个文件**，避免翻译一部分就停止

#### 🚫 内容保持不变
- ❌ **代码块**：代码保持原样不翻译，注释要翻译
- ❌ **URL**：保持原样
- ❌ **API 端点**：保持原样
- ❌ **技术标识符**：保持原样
- ❌ **参数名**：保持原样
- ❌ **Frontmatter 键**：翻译值但保持键名不变

#### ✏️ 格式保持
- ✅ 保留所有 markdown 语法
- ✅ 保留表格结构，翻译单元格内容
- ✅ 保留粗体、斜体、链接等格式
- ✅ 在英文单词和标点之间添加空格

### 步骤 4：Markdown 翻译示例

**原文（中文）：**
```markdown
# 房间管理

房间是 ZEGOCLOUD 提供的音视频空间服务，用于组织用户组。同一房间内的用户可以互相发送和接收实时音视频和消息。

## 创建房间

使用 `createRoom` 方法创建房间：

\`\`\`javascript
const roomID = 'room123';
engine.createRoom(roomID);
\`\`\`
```

**译文（英文）：**
```markdown
# Room Management

A room is the audio and video space service provided by ZEGOCLOUD, used to organize user groups. Users in the same room can send and receive real-time audio, video, and messages to each other.

## Create a Room

Use the `createRoom` method to create a room:

\`\`\`javascript
const roomID = 'room123';
engine.createRoom(roomID);
\`\`\`
```

---

## OpenAPI YAML 翻译工作流

### 步骤 1：收集待翻译文件

**收集指定目录下所有** `.yaml` 结尾的 OpenAPI 配置文件

**向用户展示：**
```
找到 X 个 YAML 文件需要翻译：

1. path/to/api1.yaml (123 行)
2. path/to/api2.yaml (456 行)
...

是否开始翻译这些文件？(请确认)
```

⚠️ **必须等待用户明确确认后再继续**

### 步骤 2：创建翻译任务列表

根据文件大小和优先级组织任务：

**排序规则：**
- 优先翻译小文件（行数少的在前）
- 相同大小的文件按文件名字母顺序

**分段策略：**
- **< 100 行**：直接整个文件翻译
- **≥ 100 行**：分段翻译，每段不超过 2000 行
  - 不需要额外确认，逐段翻译即可
  - 保持上下文连贯性

**内容复用：**
- 很多平台的同名文件有重复内容
- 翻译时发现相同内容可以直接复用已翻译的文本
- 记录已翻译的段落供后续复用

### 步骤 3：OpenAPI YAML 翻译执行

**必须遵守的规则：**

#### 📋 翻译前准备
- ✅ **必须先阅读术语对照表**，了解专业术语的标准翻译
- ✅ **核心技术概念以参考翻译为准**，保持一致性

#### 🎯 翻译重点
- ✅ **重点翻译接口、参数的描述**
- ❌ **禁止翻译 OpenAPI 关键字**（如 `info`, `paths`, `get`, `post`, `parameters`, `responses`, `schema` 等）
- ✅ 只翻译 `description`, `summary`, `example` 等描述性字段的值

#### 🔤 标点符号处理
- ✅ 所有中文标点符号转为英文标点符号
- ✅ **特殊规则**：如果描述是单行且包含中文冒号 `：`，必须改为多行描述（使用 `|`）

**示例：**
```yaml
# 原始中文（单行）
description: 接口名称：获取用户列表

# 错误翻译（仍是单行）
description: Interface name: Get user list

# 正确翻译（多行）
description: |
  Interface name: Get user list
```

#### ⚠️ 转义字符处理
- ✅ **保留原有的反斜杠转义符**，不要删除

#### 📝 内容准确性
- ✅ **忠于原文**，禁止随意扩写或捏造内容
- ✅ **链接地址**可以按中英文实际情况调整
- ✅ **以 `/` 开头的内部链接名称**优先使用 `sidebars.json` 中定义的 label
- ✅ **必须完整翻译每个文件**，避免翻译一部分就停止
- ✅ **翻译结果不能出现中文和中文标点符号**，杜绝中英混杂

#### ✏️ 格式保持
- ✅ 保留 YAML 结构和缩进
- ✅ 保持键名不变，只翻译描述性值
- ✅ 保留所有特殊字符和格式标记

### 步骤 4：OpenAPI YAML 翻译示例

**原文（中文）：**
```yaml
info:
  title: 用户管理 API
  description: 提供用户相关的接口，包括创建、查询、更新、删除等操作
  version: 1.0.0

paths:
  /users:
    get:
      summary: 获取用户列表
      description: 获取所有用户的列表，支持分页和筛选
      parameters:
        - name: page
          in: query
          description: 页码，从 1 开始
          required: false
          schema:
            type: integer
        - name: limit
          in: query
          description: 每页数量：默认 10，最大 100
          required: false
          schema:
            type: integer
```

**译文（英文）：**
```yaml
info:
  title: User Management API
  description: |
    Provides user-related interfaces, including create, query, update, delete operations
  version: 1.0.0

paths:
  /users:
    get:
      summary: Get user list
      description: Get the list of all users, supports pagination and filtering
      parameters:
        - name: page
          in: query
          description: Page number, starting from 1
          required: false
          schema:
            type: integer
        - name: limit
          in: query
          description: |
          Items per page: Default 10, maximum 100
          required: false
          schema:
            type: integer
```

---

## 批量文件翻译工作流

适用于新产品上线或大规模文档翻译场景。

### 步骤 1：扫描目录并生成翻译计划

使用 `scan_translation_files.py` 脚本扫描指定目录：

**使用方法：**
```bash
python3 .skills/zh-translator/scripts/scan_translation_files.py <目录路径> [每批行数]
```

**参数说明：**
- `<目录路径>`：要扫描的目录，如 `docs/zh/product`
- `[每批行数]`：可选，默认 500 行，控制每批翻译的总量

**示例：**
- 默认批次大小：`python3 .skills/zh-translator/scripts/scan_translation_files.py docs/zh/product`
- 自定义批次：`python3 .skills/zh-translator/scripts/scan_translation_files.py docs/zh/product 300`

**输出内容：**
1. **统计摘要**：
   - API 文件数量（仅需翻译 YAML）
   - Markdown 文件数量和行数
   - YAML 文件数量和行数
   - 总批次和平均每批行数
   - 大文件列表（>500 行）

2. **批次计划**：
   - 每批包含的文件列表
   - 每批的总行数和文件数
   - 大文件标记（需要分段翻译）

3. **JSON 数据**：供后续处理使用

**智能识别规则：**
- ✅ 自动识别 `server` 平台 `api-reference` 目录下的同名 `.mdx` 和 `.yaml` 文件对
- ✅ 对于成对文件，**仅翻译 `.yaml`**，`.mdx` 是自动生成的
- ✅ 自动按文件大小分类：
  - **小文件**（< 100 行）：多个文件一批
  - **中等文件**（100-500 行）：1-2 个文件一批
  - **大文件**（> 500 行）：单独成批，翻译时分段处理

### 步骤 2：展示翻译计划并确认

向用户展示扫描结果，等待确认：

```
📊 翻译扫描结果
- API 文件：X 个（Y 行）
- Markdown 文件：X 个（Y 行）
- YAML 文件：X 个（Y 行）
- 总批次：Z 批
⚠️ 大文件：X 个（需要分段翻译）

是否开始按批次翻译？请确认。
```

⚠️ **必须等待用户明确确认后再继续**

### 步骤 3：逐批次翻译

#### 3.1 翻译批次策略

**每个批次翻译前：**
```
📦 开始翻译批次 1/Z（包含 X 个文件，共 Y 行）
文件列表：
1. path/to/file1.md (123 行)
2. path/to/file2.yaml (67 行)
...

正在翻译...
```

**批次翻译完成后：**
```
✅ 批次 1/Z 翻译完成
- 已翻译文件：X 个
- 翻译行数：Y 行

是否继续翻译下一批？（批次 2/Z）
```

⚠️ **每批完成后必须暂停并等待用户确认**

#### 3.2 大文件分段翻译

对于大文件（> 500 行），采用分段策略：

**分段规则：**
- 每段不超过 2000 行
- 保持段落完整性（尽量在章节边界分段）
- 第一段翻译完成并保存后，继续下一段

**大文件处理流程：**
```
⚠️ 处理大文件：path/to/large_file.md (2500 行)
📍 第 1/2 段（第 1-1250 行）
[翻译第 1 段...]

✅ 第 1 段完成
📍 第 2/2 段（第 1251-2500 行）
[翻译第 2 段...]

✅ 大文件翻译完成：path/to/large_file.md
```

#### 3.3 批次内翻译规则

**每个批次内的文件翻译：**
- 按照文件列表顺序逐个翻译
- 每个文件遵循其类型的翻译规则（Markdown 或 YAML）
- 加载适用的术语对照表
- 翻译完成后立即报告进度

### 步骤 4：批次翻译进度报告

**每批翻译完成后的报告：**
```
✅ 批次 1/Z 翻译完成
详细进度：
  ✅ file1.md → file1.md (123 行)
  ✅ file2.yaml → file2.yaml (67 行)
  ...

本批次统计：
- 翻译文件数：X
- 翻译行数：Y
- 使用术语表：common, <产品名>

当前总进度：
- 已完成批次：1/Z
- 已翻译文件：X/Y
- 已翻译行数：A/B
```

**全部完成后的总结：**
```
🎉 全部批次翻译完成！
最终统计：
- 总批次：Z
- 总文件数：X
- 总行数：Y
- 使用术语表：common, <产品1>, <产品2>, ...

耗时统计：
- API 文件：X 个
- Markdown 文件：Y 个
- YAML 文件：Z 个
- 大文件分段：W 段
```

### 步骤 5：批量翻译特殊规则

#### 📋 批次翻译前准备
- ✅ **预先加载所有相关术语表**
- ✅ **识别所有文件对应的产品线**
- ✅ **确认文件类型分类正确**

#### 🔤 API 文件特殊处理
- ✅ **严格跳过 `.mdx` 文件**，不翻译
- ✅ **仅翻译 `.yaml` 文件**
- ✅ 在批次报告中标注跳过的 mdx 文件数量

#### 📝 大文件分段处理
- ✅ **保持上下文连贯性**，段与段之间术语一致
- ✅ **段间衔接处**检查翻译连贯性
- ✅ **分段信息记录**，便于追溯

#### ⚠️ 错误处理
- ✅ **单个文件翻译失败**：记录错误，继续批次内其他文件
- ✅ **批次失败处理**：询问用户是否重试当前批次
- ✅ **保存翻译进度**：已完成批次不重复翻译

#### ✏️ 进度保存
- ✅ **记录已完成批次**：便于中断后恢复
- ✅ **生成批次日志**：每批翻译的文件和状态
- ✅ **错误文件清单**：需要人工复查的文件

---

## 通用翻译规则（三种类型都适用）

### 进度报告

**每个文件/段落翻译完成后报告：**
```
✅ 已翻译：path/to/source.md → path/to/target.md
```

**全部完成后提供总结：**
```
🎉 翻译完成！
- 翻译文件数：X
- 翻译行数：Y
- 使用术语表：common, <产品名>
```

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

## 术语对照表维护

### 术语表位置
- 通用术语：`.translate/common-terminology.csv`
- 产品术语：`.translate/products/<产品ID>.csv`

### 术语表格式
```csv
CN,EN
中文术语,English Term 1 / Alternative 2
另一个术语,Another English Term
```

### 遇到新术语时
1. 根据上下文和通用用法翻译
2. 记录下来，后续可以考虑添加到术语表
3. 在当前文档中保持翻译一致性

## 资源文件

### scripts/
- **analyze_changes.py**：Git 变更分析脚本，用于识别改动的 markdown 文件
- **scan_translation_files.py**：目录扫描脚本，用于批量翻译场景
  - 递归扫描指定目录下的所有文件
  - 自动识别 API 文件对（mdx + yaml）
  - 生成分批次翻译计划
  - 按文件大小智能分类和分组

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