# 完整翻译工作流程

## 流程概览

```
1. 扫描文档
   ↓
2. 准备目标目录
   ↓
3. 预处理全复用文档（必选）
   ↓
4. 创建进度报告
   ↓
5. 加载术语对照表
   ↓
6. 逐批次翻译
   ↓
7. 恢复翻译（如需要）
```

---

## 详细步骤

### 第一步：扫描文档

**脚本**：`scripts/scan_batch_translation.py`

**命令**：
```bash
python3 .claude/skills/trans-batch/scripts/scan_batch_translation.py <源目录> > scan_result.json
```

**示例**：
```bash
python3 .claude/skills/trans-batch/scripts/scan_batch_translation.py \
  core_products/real-time-voice-video/zh/flutter > scan_result.json
```

**输出**：
- 统计摘要（API 文档、全复用文档、普通文档等）
- 翻译批次计划
- JSON 格式的扫描结果（保存为 `scan_result.json`）

---

### 第二步：准备目标目录

**检查目标英文目录是否存在**：
- 如果**不存在**：执行 `cp -r <zh-source> <en-target>` 完全拷贝内容
- 如果**已存在**：直接使用现有目录

**命令**：
```bash
# 检查并拷贝（如果需要）
zh_source="core_products/real-time-voice-video/zh/flutter"
en_target="core_products/real-time-voice-video/en/flutter"

if [ ! -d "$en_target" ]; then
    cp -r "$zh_source" "$en_target"
    echo "✅ 已拷贝源目录到目标目录"
else
    echo "✅ 目标目录已存在，直接使用"
fi
```

---

### 第三步：预处理全复用文档（必选）

**脚本**：`scripts/preprocess_reuse_docs.py`

**命令**：
```bash
python3 .claude/skills/trans-batch/scripts/preprocess_reuse_docs.py scan_result.json > preprocess_result.json
```

**处理逻辑**：
1. 读取所有"全复用文档"列表
2. 对每个文件：
   - 提取 import 路径
   - 将路径中的 `/zh/` 替换为 `/en/`
   - 检查对应的英文文档是否存在
   - 如果存在：替换路径并保存，标记为"已解决"
   - 如果不存在：标记为"需要翻译"

**输出**：
- 每个文件的处理结果
- JSON 格式的预处理结果（保存为 `preprocess_result.json`）

---
### 第四步：创建进度报告

**脚本**：`scripts/progress_manager.py`

**命令**：
```bash
python3 .claude/skills/trans-batch/scripts/progress_manager.py create \
  <目标目录> \
  <源目录> \
  scan_result.json \
  preprocess_result.json
```

**示例**：
```bash
python3 .claude/skills/trans-batch/scripts/progress_manager.py create \
  core_products/real-time-voice-video/en/flutter \
  core_products/real-time-voice-video/zh/flutter \
  scan_result.json \
  preprocess_result.json
```

**输出**：
- 在目标目录下创建 `.translation-progress.json` 文件
- 包含完整的翻译计划和进度跟踪信息

---

### 第五步：按批次翻译

#### 5.1 加载术语对照表（每次都要重新加载）

**⚠️ 重要**：每次用户说"继续翻译"时，都必须重新加载术语对照表到上下文

**加载顺序**：
1. **通用术语表**：`.translate/common-terminology.csv`
2. **产品特定术语表**：`.translate/products/<产品ID>.csv`

**产品识别映射**：
- `real_time_video` / `real_time_voice` / `rtc` → `real_time_video_zh.csv`
- `zim` / `imkit` → `zim_zh.csv`
- `callkit` → `callkit_zh.csv`
- `live_streaming_kit` / `live_audio_room_kit` → `live_streaming_kit_zh.csv`
- `super_board` → `super_board_zh.csv`
- `ai_effects` → `ai_effects_zh.csv`

**加载命令**：
```bash
# 读取通用术语表
cat .translate/common-terminology.csv

# 读取产品特定术语表（根据产品识别）
cat .translate/products/real_time_video_zh.csv
```

#### 5.2 查看当前批次

**命令**：
```bash
python3 .claude/skills/trans-batch/scripts/progress_manager.py current <目标目录>
```

**输出**：
- 当前批次号
- 待翻译文件列表
- 已完成文件列表

#### 5.3 逐个翻译文件

**翻译完成后标记文件状态**：
```bash
python3 .claude/skills/trans-batch/scripts/progress_manager.py update-file \
  <目标目录> \
  <源文件路径> \
  <目标文件路径> \
  <批次号>
```

**示例**：
```bash
python3 .claude/skills/trans-batch/scripts/progress_manager.py update-file \
  core_products/real-time-voice-video/en/flutter \
  core_products/real-time-voice-video/zh/flutter/intro.mdx \
  core_products/real-time-voice-video/en/flutter/intro.mdx \
  1
```

**如果翻译失败**：
```bash
python3 .claude/skills/trans-batch/scripts/progress_manager.py fail-file \
  <目标目录> \
  <源文件路径> \
  <错误信息> \
  <批次号>
```

#### 5.4 标记批次完成

**命令**：
```bash
python3 .claude/skills/trans-batch/scripts/progress_manager.py update-batch \
  <目标目录> \
  <批次号>
```

**时机**：批次所有文件翻译完成后

#### 5.5 查看总体进度

**命令**：
```bash
python3 .claude/skills/trans-batch/scripts/progress_manager.py show <目标目录>
```

**输出**：
- 批次进度（已完成/总数）
- 文件进度（已翻译/总数）
- 行数进度（已翻译/总数）
- 跳过的文件及原因
- 失败的文件及错误

#### 5.6 继续下一批

**⚠️ 重要**：每次继续翻译下一批时，必须：
1. **重新加载术语对照表**到上下文
2. 查看当前批次
3. 重复 5.3-5.5

---

### 第六步：进度恢复

**场景**：翻译任务意外终止后恢复

**恢复步骤**：

1. **查看当前进度**：
   ```bash
   python3 .claude/skills/trans-batch/scripts/progress_manager.py show <目标目录>
   ```

2. **查看当前批次**：
   ```bash
   python3 .claude/skills/trans-batch/scripts/progress_manager.py current <目标目录>
   ```

3. **重新加载术语对照表**：
   ```bash
   cat .translate/common-terminology.csv
   cat .translate/products/<产品ID>.csv
   ```

4. **从 current_batch 继续翻译**，跳过已完成的批次和文件

---

## 大文件分段翻译

**触发条件**：单个文件超过 2000 行

**处理方式**：

```
⚠️ 处理大文件：path/to/large_file.mdx (2500 行)
📍 第 1/2 段（第 1-1250 行）
[翻译第 1 段...]

✅ 第 1 段完成
📍 第 2/2 段（第 1251-2500 行）
[翻译第 2 段...]

✅ 大文件翻译完成：path/to/large_file.mdx
```

**注意**：
- 分段翻译时，只标记一次文件完成
- 确保所有段落都翻译完成后再标记

---

## 批次分配策略

### 小文件（< 50 行）
- **每批文件数**：10-20 个
- **总行数控制**：不超过 1000 行
- **翻译速度**：快速，可以批量处理

### 中等文件（50-300 行）
- **每批文件数**：2-5 个
- **总行数控制**：不超过 1500 行
- **翻译速度**：适中，需要适度关注

### 大文件（> 300 行）
- **每批文件数**：1 个
- **分段处理**：如果超过 2000 行，需要分段
- **翻译速度**：较慢，需要更多时间

---

## 常见问题

### Q: 如何知道哪些文件被跳过了？

**A**: 查看进度报告的 `skipped_files` 字段，每个跳过的文件都有详细的 `reason` 和 `reason_code`。

### Q: 预处理失败怎么办？

**A**: 检查 `preprocess_result.json` 中的失败信息，常见的失败原因：
- import 路径格式不正确
- 文件权限问题
- 英文文档路径不存在

### Q: 进度文件损坏怎么办？

**A**: 可以重新运行 `progress_manager.py create`，它会覆盖现有的进度文件。

### Q: 如何查看翻译了多少内容？

**A**: 运行 `progress_manager.py show <目标目录>`，查看 `translated_files` 和 `translated_lines` 字段。
