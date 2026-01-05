# 使用示例

## 示例 1：翻译 Flutter 文档

### 场景

批量翻译 `core_products/real-time-voice-video/zh/flutter` 目录下的所有中文文档到英文。

### 完整流程

```bash
# 1. 扫描文档
python3 .claude/skills/trans-batch/scripts/scan_batch_translation.py \
  core_products/real-time-voice-video/zh/flutter > scan_result.json

# 输出示例：
# 📊 批量翻译扫描结果
# ⏭️  API 文档（docType: API，自动跳过）：4 个
# 🔄 全复用文档（需要预处理）：4 个
# 📄 普通文档分类：
#    小文件（< 50 行）：3 个
#    中等文件（50-300 行）：1 个
# 📊 翻译任务统计：
#    需翻译文件数：8
#    需翻译总行数：112
#    翻译批次数：2


# 2. 准备目标目录
zh_source="core_products/real-time-voice-video/zh/flutter"
en_target="core_products/real-time-voice-video/en/flutter"

if [ ! -d "$en_target" ]; then
    cp -r "$zh_source" "$en_target"
    echo "✅ 已拷贝源目录到目标目录"
else
    echo "✅ 目标目录已存在，直接使用"
fi

# 3. 预处理全复用文档（必选）
python3 .claude/skills/trans-batch/scripts/preprocess_reuse_docs.py \
  scan_result.json > preprocess_result.json

# 输出示例：
# 🔄 开始预处理全复用文档：4 个
# [1/4] 处理：faq.mdx
#    ✅ 已解决：@site/zh/rtc/faq → @site/en/rtc/faq
# [2/4] 处理：overview.mdx
#    ⚠️  需要翻译：英文文档不存在
# ...


# 4. 创建进度报告
python3 .claude/skills/trans-batch/scripts/progress_manager.py create \
  core_products/real-time-voice-video/en/flutter \
  core_products/real-time-voice-video/zh/flutter \
  scan_result.json \
  preprocess_result.json

# 输出：
# ✅ 进度文件已保存：core_products/real-time-voice-video/en/flutter/.translation-progress.json
# 📊 翻译进度摘要
# 批次进度：0/2
# 文件进度：0/8
# 行数进度：0/112

# 5. 开始翻译第一批
# 5.1 加载术语对照表
cat .translate/common-terminology.csv
cat .translate/products/real_time_video_zh.csv

# 5.2 查看当前批次
python3 .claude/skills/trans-batch/scripts/progress_manager.py current \
  core_products/real-time-voice-video/en/flutter

# 输出：
# 🔄 当前批次：1/2
# 批次信息：34 行, 3 个文件
# 待翻译文件：3 个
#   1. client-sdk/download-sdk.mdx (20 行)
#   2. client-sdk/release-notes.mdx (14 行)
#   3. client-sdk/download-demo.mdx (0 行)

# 5.3 翻译第一个文件
# ... 手动翻译 client-sdk/download-sdk.mdx ...

# 5.4 标记文件完成
python3 .claude/skills/trans-batch/scripts/progress_manager.py update-file \
  core_products/real-time-voice-video/en/flutter \
  core_products/real-time-voice-video/zh/flutter/client-sdk/download-sdk.mdx \
  core_products/real-time-voice-video/en/flutter/client-sdk/download-sdk.mdx \
  1

# 输出：✅ 文件已标记为完成

# 5.5 重复 5.3-5.4 翻译其他文件
# ... 翻译 client-sdk/release-notes.mdx ...
# ... 翻译 client-sdk/download-demo.mdx ...

# 5.6 标记批次完成
python3 .claude/skills/trans-batch/scripts/progress_manager.py update-batch \
  core_products/real-time-voice-video/en/flutter \
  1

# 输出：✅ 批次 1 已标记为完成

# 5.7 查看总体进度
python3 .claude/skills/trans-batch/scripts/progress_manager.py show \
  core_products/real-time-voice-video/en/flutter

# 输出：
# 📊 翻译进度摘要
# 批次进度：1/2
# 文件进度：3/8
# 行数进度：34/112

# 6. 继续翻译第二批
# ⚠️ 重要：每次继续翻译前都要重新加载术语对照表
cat .translate/common-terminology.csv
cat .translate/products/real_time_video_zh.csv

# 然后重复步骤 5.2-5.7
```

---

## 示例 2：翻译 React Native 文档

### 场景

批量翻译 `core_products/zim/zh/react-native` 目录下的所有中文文档到英文。

### 关键差异

与 Flutter 示例的主要差异：

1. **产品不同**：使用 ZIM 产品的术语表
2. **文件数量**：可能有不同的文件数量和行数
3. **批次分配**：根据文件大小自动调整批次

### 核心命令

```bash
# 1. 扫描
python3 .claude/skills/trans-batch/scripts/scan_batch_translation.py \
  core_products/zim/zh/react-native > scan_result.json

# 2. 准备目标目录
cp -r core_products/zim/zh/react-native core_products/zim/en/react-native

# 3. 预处理
python3 .claude/skills/trans-batch/scripts/preprocess_reuse_docs.py \
  scan_result.json > preprocess_result.json


# 4. 创建进度报告
python3 .claude/skills/trans-batch/scripts/progress_manager.py create \
  core_products/zim/en/react-native \
  core_products/zim/zh/react-native \
  scan_result.json \
  preprocess_result.json

# 5. 翻译（每次都要重新加载术语表）
cat .translate/common-terminology.csv
cat .translate/products/zim_zh.csv  # 注意：ZIM 产品术语表

# 然后逐批次翻译...
```

---

## 示例 3：处理大文件

### 场景

翻译一个 2500 行的大文件 `advanced-features.mdx`。

### 处理方式

```bash
# 1. 查看当前批次
python3 .claude/skills/trans-batch/scripts/progress_manager.py current \
  core_products/rtc/en/flutter

# 输出：
# 🔄 当前批次：5/20
# 批次信息：2500 行, 1 个文件
# ⚠️  此批次包含超大文件，翻译时需要分段处理（每段不超过 2000 行）
# 待翻译文件：1 个
#   1. advanced/advanced-features.mdx (2500 行) [大文件]

# 2. 加载术语表
cat .translate/common-terminology.csv
cat .translate/products/real_time_video_zh.csv

# 3. 分段翻译
# 第 1 段：第 1-1250 行
# ... 翻译第 1-1250 行 ...

# 第 2 段：第 1251-2500 行
# ... 翻译第 1251-2500 行 ...

# 4. 标记文件完成（只标记一次）
python3 .claude/skills/trans-batch/scripts/progress_manager.py update-file \
  core_products/rtc/en/flutter \
  core_products/rtc/zh/flutter/advanced/advanced-features.mdx \
  core_products/rtc/en/flutter/advanced/advanced-features.mdx \
  5

# 5. 标记批次完成
python3 .claude/skills/trans-batch/scripts/progress_manager.py update-batch \
  core_products/rtc/en/flutter \
  5
```

---

## 示例 4：恢复翻译

### 场景

翻译任务中途意外终止，需要从断点恢复。

### 恢复步骤

```bash
# 1. 查看当前进度
python3 .claude/skills/trans-batch/scripts/progress_manager.py show \
  core_products/rtc/en/flutter

# 输出：
# 📊 翻译进度摘要
# 批次进度：5/20
# 文件进度：45/203
# 行数进度：4320/38300
# 当前批次：6
# 状态：in_progress

# 2. 查看当前批次（批次 6）
python3 .claude/skills/trans-batch/scripts/progress_manager.py current \
  core_products/rtc/en/flutter

# 输出：
# 🔄 当前批次：6/20
# 待翻译文件：5 个
# 已完成文件：0 个

# 3. 重新加载术语表
cat .translate/common-terminology.csv
cat .translate/products/real_time_video_zh.csv

# 4. 从批次 6 继续翻译
# ... 逐个翻译批次 6 的文件并标记完成 ...

# 5. 标记批次 6 完成
python3 .claude/skills/trans-batch/scripts/progress_manager.py update-batch \
  core_products/rtc/en/flutter \
  6

# 6. 继续后续批次...
```

---

## 示例 5：处理翻译失败

### 场景

翻译某个文件时遇到错误，需要记录失败并继续。

### 处理步骤

```bash
# 1. 尝试翻译文件
# ... 翻译 process/video.mdx ...
# 遇到错误：无法理解某个技术术语

# 2. 标记文件失败
python3 .claude/skills/trans-batch/scripts/progress_manager.py fail-file \
  core_products/rtc/en/flutter \
  core_products/rtc/zh/flutter/process/video.mdx \
  "无法理解术语：'视频流预处理机制'" \
  3

# 输出：⚠️  文件已标记为失败

# 3. 继续翻译批次中的其他文件
# ... 翻译其他文件并标记完成 ...

# 4. 批次其他文件都完成后，稍后回来处理失败的文件

# 5. 查看失败文件列表
python3 .claude/skills/trans-batch/scripts/progress_manager.py show \
  core_products/rtc/en/flutter

# 输出包含：
# ❌ 失败的文件：1 个
#    - core_products/rtc/zh/flutter/process/video.mdx
#      错误：无法理解术语：'视频流预处理机制'

# 6. 询问用户或查找相关资料后，重新翻译失败的文件
# ... 重新翻译 ...
# 翻译成功后标记完成
python3 .claude/skills/trans-batch/scripts/progress_manager.py update-file \
  core_products/rtc/en/flutter \
  core_products/rtc/zh/flutter/process/video.mdx \
  core_products/rtc/en/flutter/process/video.mdx \
  3
```

---

## 常见使用模式

### 模式 1：批量翻译小文件

```bash
# 适用于：文件多但每个文件都很小（< 50 行）
# 特点：翻译速度快，一批可以处理 10-20 个文件

# 1. 扫描
python3 .claude/skills/trans-batch/scripts/scan_batch_translation.py <源目录>

# 2. 预处理
python3 .claude/skills/trans-batch/scripts/preprocess_reuse_docs.py scan_result.json

# 3. 创建进度
python3 .claude/skills/trans-batch/scripts/progress_manager.py create <目标目录> <源目录> scan_result.json preprocess_result.json

# 4. 快速翻译多个文件
for file in $(cat file_list.txt); do
    # 翻译文件
    # 标记完成
done
```

### 模式 2：处理中等文件

```bash
# 适用于：文件数量适中，每个文件 50-300 行
# 特点：需要适度关注，一批处理 2-5 个文件

# 与模式 1 类似，但每批文件数较少
# 每个文件需要更多时间检查质量
```

### 模式 3：处理大文件

```bash
# 适用于：文件数量少，但单个文件 > 300 行
# 特点：每个文件单独一批，可能需要分段

# 见"示例 3：处理大文件"
```

---

## 注意事项

### 术语表加载时机

⚠️ **每次用户说"继续翻译"时，都必须重新加载术语对照表**

```bash
# 错误示例：只在开始时加载一次
cat .translate/common-terminology.csv
# 翻译批次 1...
# 翻译批次 2... ← 术语表可能已不在上下文中

# 正确示例：每批都重新加载
cat .translate/common-terminology.csv
# 翻译批次 1...
cat .translate/common-terminology.csv  # 重新加载
# 翻译批次 2...
```

### 预处理是必选步骤

不要跳过预处理步骤，即使没有全复用文档也要执行，因为它会：
1. 检查文件引用
2. 更新扫描结果
3. 为进度报告提供完整信息

### 进度更新要及时

翻译完每个文件后立即标记完成，不要等到批次结束才批量标记。这样可以：
1. 实时保存进度
2. 防止意外中断导致进度丢失
3. 方便查看当前状态
