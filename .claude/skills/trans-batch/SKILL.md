---
name: trans-batch
description: 批量翻译新产品文档。智能扫描中文目录，自动过滤API文档、YAML生成的MDX等不需要翻译的文件，预处理全复用文档，按文件大小分批翻译。触发词：批量翻译、新产品翻译、批量文档翻译、trans-batch。使用场景：(1) 翻译新产品所有中文文档到英文 (2) 批量翻译目录下所有文件 (3) 需要进度跟踪和断点续传的大规模翻译任务 (4) 查漏补缺，检查并翻译遗漏的文档。
---

# 批量翻译新产品文档

## ⚠️ 重要要求

**所有脚本必须在 workspace 根目录下运行**,以确保正确解析文件路径。

Workspace 根目录通过以下标记文件识别:
- `docuo.config.json` 或 `docuo.config.en.json` (DOCUO 项目)
- `.git` (Git 仓库)
- `package.json` (Node.js 项目)

**正确运行方式**:
```bash
# 确保在 workspace 根目录
cd /path/to/workspace
pwd  # 应该显示 workspace 根目录

# 然后运行脚本
python3 .claude/skills/trans-batch/scripts/scan_batch_translation.py <source_dir>
```

**错误示例**:
```bash
# ❌ 错误:在子目录中运行
cd core_products/real-time-voice-video/zh/flutter
python3 ../../../.claude/skills/trans-batch/scripts/scan_batch_translation.py .

# ✅ 正确:在 workspace 根目录运行
cd /path/to/workspace
python3 .claude/skills/trans-batch/scripts/scan_batch_translation.py \
  core_products/real-time-voice-video/zh/flutter
```

## 快速开始

```
/trans-batch <中文源目录>
```

**示例**：
```
/trans-batch core_products/real-time-voice-video/zh/flutter
/trans-batch core_products/zim/zh/react-native
```

## 工作流程

### 模式 A：完整批量翻译（推荐新产品）

**步骤 0-5**：翻译新产品所有文档

### 1. 扫描文档
```bash
# 脚本会自动将 scan_result.json 保存到目标目录（与 sidebars.json 同级）
python3 .claude/skills/trans-batch/scripts/scan_batch_translation.py <源目录>
```

**说明**：
- 脚本会自动计算目标目录（将源目录的 `/zh/` 替换为 `/en/`）
- 例如：源目录 `core_products/real-time-voice-video/zh/flutter` → 输出到 `core_products/real-time-voice-video/en/flutter/scan_result.json`
- 如需自定义输出目录：`--output-dir <自定义路径>`
- 兼容旧版本：添加 `--stdout` 参数可输出到 stdout（需要手动重定向）

### 2. 准备目标目录
```bash
# 检查目标目录是否存在，不存在则拷贝
zh_source="<源目录>"
en_target="<目标目录>"
if [ ! -d "$en_target" ]; then
    cp -r "$zh_source" "$en_target"
fi
```

### 3. 预处理全复用文档（必选）
```bash
# 脚本会自动将 preprocess_result.json 保存到目标目录（与 scan_result.json 同级）
python3 .claude/skills/trans-batch/scripts/preprocess_reuse_docs.py <目标目录>/scan_result.json
```

**说明**：
- 脚本会从 `scan_result.json` 读取 `target_directory` 字段，自动输出到同一目录
- 输出文件：`<目标目录>/preprocess_result.json`
- 如需自定义输出目录：`--output-dir <自定义路径>`
- 兼容旧版本：添加 `--stdout` 参数可输出到 stdout（需要手动重定向）

### 4. 创建进度报告
```bash
python3 .claude/skills/trans-batch/scripts/progress_manager.py create \
  <目标目录> <源目录> <目标目录>/scan_result.json <目标目录>/preprocess_result.json
```

### 5. 逐批次翻译

**⚠️ 重要：每次用户说"继续翻译"时，都要重新加载术语对照表**

```bash
# 5.1 加载术语对照表（每次都要）
cat .translate/common-terminology.csv
cat .translate/products/<产品ID>.csv

# 5.2 查看当前批次
python3 .claude/skills/trans-batch/scripts/progress_manager.py current <目标目录>

# 5.3 翻译文件并标记完成
python3 .claude/skills/trans-batch/scripts/progress_manager.py update-file \
  <目标目录> <源路径> <目标路径> <批次号>

# 5.4 标记批次完成
python3 .claude/skills/trans-batch/scripts/progress_manager.py update-batch \
  <目标目录> <批次号>

# 5.5 查看总体进度
python3 .claude/skills/trans-batch/scripts/progress_manager.py show <目标目录>

# 5.6 重复 5.1-5.5 继续下一批
```

---

### 模式 B：查漏补缺（已有英文实例）

适用场景：英文实例已存在，但部分文档未翻译。

**触发词**：用户说"查漏补缺"、"检查遗漏"、"翻译遗漏文档"

**步骤 0-5**：只翻译遗漏的文档

### 0. 检查遗漏文档

```bash
# 脚本会自动将 scan_result.json 保存到实例目录（与 sidebars.json 同级）
python3 .claude/skills/trans-batch/scripts/check_missing_translations.py \
  <英文实例目录>

# 例如：
python3 .claude/skills/trans-batch/scripts/check_missing_translations.py \
  core_products/real-time-voice-video/en/android-java
```

**说明**：
- 脚本会自动将 `scan_result.json` 保存到实例目录（传入的英文实例目录）
- 输出文件：`<英文实例目录>/scan_result.json`

### 1. 准备目标目录

```bash
# 英文实例已存在，跳过此步骤
```

### 2. 预处理全复用文档（必选）

```bash
# 脚本会自动从 scan_result.json 读取目标目录并保存到同一位置
python3 .claude/skills/trans-batch/scripts/preprocess_reuse_docs.py \
  scan_result.json
```

**说明**：
- 脚本会从 `scan_result.json` 读取 `target_directory` 字段，自动输出到同一目录
- 例如：`<英文实例目录>/preprocess_result.json`
- 兼容旧版本：添加 `--stdout` 参数可输出到 stdout（需要手动重定向）

### 3. 创建进度报告

```bash
python3 .claude/skills/trans-batch/scripts/progress_manager.py create \
  <英文实例目录> <中文源目录> scan_result.json preprocess_result.json
```

**说明**：
- 所有文件都在英文实例目录下（与 sidebars.json 同级）
- 例如：`core_products/real-time-voice-video/en/android-java/scan_result.json`

### 4. 逐批次翻译

（同模式 A 步骤 5）

**关键差异**：
- 模式 A：扫描中文源目录，翻译所有文档
- 模式 B：扫描英文实例 sidebars.json，只翻译遗漏文档

## 文件分类

详细的文件分类规则见 [references/file-classification.md](references/file-classification.md)

**简要说明**：
- **API 文档**（docType: API）：自动跳过
- **YAML+MDX 对**：只翻译 YAML，跳过 MDX（自动生成）
- **全复用文档**：预处理，尝试替换 `/zh/` 为 `/en/` 引用
- **普通文档**：按行数分批（<50、50-300、>300 行）

## 进度管理

### 查看进度
```bash
# 查看摘要
progress_manager.py show <目标目录>

# 查看当前批次
progress_manager.py current <目标目录>
```

### 更新状态
```bash
# 标记文件完成
progress_manager.py update-file <目标目录> <源路径> <目标路径> <批次号>

# 标记批次完成
progress_manager.py update-batch <目标目录> <批次号>

# 标记文件失败
progress_manager.py fail-file <目标目录> <源路径> <错误信息> <批次号>
```

### 恢复翻译

如果翻译任务意外终止：
1. 查看 `progress_manager.py show <目标目录>` 获取当前状态
2. 从 `current_batch` 继续翻译
3. **重新加载术语对照表**

## 翻译质量

详细的翻译规则见 [references/quality-rules.md](references/quality-rules.md)

**核心原则**：
- ✅ 必须使用术语对照表（每次都要重新加载）
- ✅ 中文标点转为英文标点
- ✅ 代码、URL、API 保持不变
- ✅ 手动翻译，禁止自动化工具

**术语表映射**：
- `real_time_video` / `rtc` → `real_time_video_zh.csv`
- `zim` → `zim_zh.csv`
- `callkit` → `callkit_zh.csv`
- `live_streaming_kit` → `live_streaming_kit_zh.csv`
- `super_board` → `super_board_zh.csv`
- `ai_effects` → `ai_effects_zh.csv`

## 批次策略

- **小文件**（< 50 行）：每批 10-20 个文件，≤1000 行
- **中等文件**（50-300 行）：每批 2-5 个文件，≤1500 行
- **大文件**（> 300 行）：单独成批，>2000 行需分段

## 更多信息

- **完整工作流程**：[references/translation-workflow.md](references/translation-workflow.md)
- **文件分类详情**：[references/file-classification.md](references/file-classification.md)
- **翻译质量规则**：[references/quality-rules.md](references/quality-rules.md)
- **使用示例**：[references/examples.md](references/examples.md)

## 资源文件

### scripts/
- **check_missing_translations.py**：查漏补缺，扫描英文实例找出所有未翻译文档，默认输出 scan_result.json 格式
- **scan_batch_translation.py**：扫描和分类文档，生成翻译计划
- **preprocess_reuse_docs.py**：预处理全复用文档，替换引用路径
- **progress_manager.py**：管理翻译进度，记录文件状态和批次进度
- **batch_translate.py**：整合所有步骤的编排脚本

### .translate/
- **common-terminology.csv**：通用术语表
- **products/**：产品特定术语表

## 重要说明

### 📁 文件组织（支持并发）

所有中间文件（scan_result.json、preprocess_result.json、scan_result_clean.json）现在都**自动保存到实例目录**（与 sidebars.json 同级），而不是 workspace 根目录。

**优点**：
- ✅ 支持并发执行多个翻译任务（每个实例的文件互不冲突）
- ✅ 文件与对应实例关联，易于管理
- ✅ 自动计算目标目录，减少手动指定路径

**示例文件结构**：
```
core_products/real-time-voice-video/en/flutter/
  ├── sidebars.json
  ├── scan_result.json          # 自动保存到实例目录
  ├── preprocess_result.json    # 自动保存到实例目录
  ├── .translation-progress.json
  └── ...
```

### ⚠️ 禁止事项

**严格禁止**：
- ❌ 创建翻译脚本自动翻译
- ❌ 调用第三方翻译 API
- ❌ 使用任何自动化翻译工具
- ❌ 批量生成翻译内容

**必须手动翻译每个文件**，确保翻译质量和准确性。

### ✅ 允许事项

**可以使用脚本**：
- ✅ 扫描目录生成文件列表
- ✅ 加载和查询术语对照表
- ✅ 文件路径转换和定位
- ✅ 预处理全复用文档（替换引用路径）
- ✅ 拷贝目录和文件
- ✅ 管理翻译进度（标记完成、失败等）

**核心原则**：脚本用于辅助分析和准备，实际翻译必须由 AI 手动完成。
