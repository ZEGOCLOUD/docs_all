---
name: update-sidebars
description: 自动更新 DOCUO 侧边栏标签,从 MDX 文件中提取 H1 标题。触发词:更新侧边栏、update sidebars、同步侧边栏标签。支持文档标签(type:doc)、内部链接(type:link)、分类标签(type:category)、属性标签(tag.label)、外部链接(https)的更新和翻译。默认直接修改文件,无需 --dry-run。
---

# 更新 DOCUO 侧边栏标签

## 概述

自动化保持 DOCUO 侧边栏标签与文档内容同步。读取 `sidebars.json`,解析文档 ID 到 MDX 文件,提取 H1 标题,更新标签。

**优势**: 消除手动更新、自动处理 DOCUO 规则、支持批量更新、详细反馈。

## 快速开始

### 1. 更新文档和内部链接标签

从 MDX 文件的 H1 提取标签并自动更新:

```bash
# 单个实例
python3 scripts/update_sidebar_labels.py path/to/instance/sidebars.json

# 批量更新
python3 scripts/update_sidebar_labels.py --all --root path/to/docs
```

### 2. 更新需要 AI 翻译的标签

分类、属性、外部链接标签需要 AI 翻译:

```bash
# 步骤 1: 收集标签(自动完成)
python3 scripts/update_sidebar_labels.py --all --root path/to/docs

# 步骤 2: AI 翻译收集到的 /en/ 标签(手动)

# 步骤 3: 应用翻译
python3 scripts/update_category_labels.py --all path/to/docs --translations '{"产品简介": "Introduction", "快速开始": "Quick Start"}'
python3 scripts/update_tag_labels.py --all path/to/docs --translations '{"基础": "Basic", "进阶": "Advanced"}'
python3 scripts/update_external_link_labels.py --all path/to/docs --translations '{"ZEGO 文档": "ZEGO Docs"}'
```

**注意**:
- 只有 /en/ 路径需要翻译,/zh/ 路径跳过。
- 禁止用 AI 翻译 type 为 doc 的节点的 label

## AI 翻译标签类型

| 标签类型 | 侧边栏节点 | 收集脚本 | 更新脚本 | 示例 |
|---------|----------|---------|---------|------|
| **分类** | `type: "category"` | update_sidebar_labels.py | update_category_labels.py | 产品简介 → Introduction |
| **属性** | `tag: {label: "..."}` | update_sidebar_labels.py | update_tag_labels.py | 基础 → Basic |
| **外部链接** | `type: "link" + href: "https://..."` | update_sidebar_labels.py | update_external_link_labels.py | ZEGO 文档 → ZEGO Docs |

**统一工作流程**:
1. `update_sidebar_labels.py` 收集并显示需要翻译的标签(只显示 /en/)
2. 使用 AI 翻译这些标签
3. 使用对应的更新脚本应用翻译结果

## 常用选项

| 选项 | 说明 |
|--------|-------------|
| `--all` | 更新目录下所有 `sidebars.json` 文件 |
| `--root PATH` | 指定 `--all` 的搜索根目录 |
| `--dry-run` | 预览更改而不修改文件 |
| `--translations` | Python dict 格式的翻译字典 |

## 验证更新

成功更新会显示 `✅ Updated: <路径>`。检查:

```bash
# 查看修改的文件
git status

# 查看具体更改
git diff path/to/sidebars.json
```

## DOCUO 核心规则

### 文档 ID 解析

- 相对于实例目录
- 无扩展名 (`.mdx`)
- 小写 + 连字符
- 移除数字前缀 (`01-`, `02-`)

**示例**: `Quick Start/Setup.mdx` → `quick-start/setup`

### H1 提取

- 跳过 frontmatter (`---` 之间)
- 提取第一个 `# 标题`
- 跳过含 HTML/过长的 H1

### 特殊处理

- **分类**: 虚拟分组,无 MDX 文件,需 AI 翻译
- **内部链接**: 自动解析到目标 MDX 并提取 H1
- **import 跟踪**: 自动从源文件提取 H1
- **不存在/无 H1**: 保持原标签,显示警告

## 输出示例

```
Processing: core_products/real-time-voice-video/en/android-java/sidebars.json
Instance directory: core_products/real-time-voice-video/en/android-java

Update: quick-start/implementing-video-call
  Old label: 实现视频通话
  New label: Implement Video Call
  Source: en/android-java/quick-start/implementing-video-call.mdx

Collect (category label): 快速开始 (locale=en)
Collect (tag label): 进阶 (in quick-start/implementing-video-call, locale=en)

✅ Updated: core_products/real-time-voice-video/en/android-java/sidebars.json

================================================================================
Category labels requiring AI translation (/en/ only):
================================================================================

EN (1 categories):
  File: core_products/real-time-voice-video/en/android-java/sidebars.json
  Label: 快速开始

================================================================================
Tag labels requiring AI translation (/en/ only):
================================================================================

EN (1 tags):
  File: core_products/real-time-voice-video/en/android-java/sidebars.json
  Context: quick-start/implementing-video-call
  Label: 进阶
```

**关键标识**:
- `Update:` - 文档标签已更改
- `Collect (category/tag label):` - 需要翻译的标签
- `Skip (no H1):` - 无 H1 标题
- `✅ Updated:` - 文件成功修改

## 故障排除

### 没有 "✅ Updated" 消息
- 检查是否有 "Update:" 消息(无则标签已是最新)
- 检查脚本退出码
- 查看完整输出

### 验证文件修改
```bash
git status
git diff path/to/sidebars.json
```

## 最佳实践

1. **批量更新前提交工作**
2. **检查 "✅ Updated" 消息**
3. **使用 git diff 验证**
4. **复用内容无 H1 是正常的**

## 脚本参考

所有脚本位于 `scripts/` 目录,可直接执行,无需加载到上下文。

- **update_sidebar_labels.py** - 更新 doc/link 标签,收集需翻译的标签
- **update_category_labels.py** - 更新 category 标签(AI 翻译)
- **update_tag_labels.py** - 更新 tag.label(AI 翻译)
- **update_external_link_labels.py** - 更新外部链接标签(AI 翻译)

详见 `references/docuo-sidebar-rules.md` 了解 DOCUO 侧边栏配置和文档 ID 规则。
