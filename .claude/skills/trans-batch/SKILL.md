---
name: trans-batch
description: 批量翻译新产品文档。智能扫描中文目录，自动过滤API文档、YAML生成的MDX等不需要翻译的文件，预处理全复用文档，按文件大小分批翻译。触发词：批量翻译、新产品翻译、批量文档翻译、trans-batch。使用场景：(1) 翻译新产品所有中文文档到英文 (2) 批量翻译目录下所有文件 (3) 需要进度跟踪和断点续传的大规模翻译任务。
---

# 批量翻译新产品文档

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

### 1. 扫描文档
```bash
python3 .claude/skills/trans-batch/scripts/scan_batch_translation.py <源目录> > scan_result.json
```

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
python3 .claude/skills/trans-batch/scripts/preprocess_reuse_docs.py scan_result.json > preprocess_result.json
```

### 4. 创建进度报告
```bash
python3 .claude/skills/trans-batch/scripts/progress_manager.py create \
  <目标目录> <源目录> scan_result.json preprocess_result.json
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
- **scan_batch_translation.py**：扫描和分类文档，生成翻译计划
- **preprocess_reuse_docs.py**：预处理全复用文档，替换引用路径
- **progress_manager.py**：管理翻译进度，记录文件状态和批次进度
- **batch_translate.py**：整合所有步骤的编排脚本

### .translate/
- **common-terminology.csv**：通用术语表
- **products/**：产品特定术语表

## 重要说明

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
