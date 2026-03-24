---
name: design-doc-structure
description: This skill should be used when the user asks to "create new document", "write documentation", "design document structure", "rewrite document", "从头写文档", "新建文档", "创建文档", "重写文档", or requests to start writing a new ZEGO technical document from scratch. Supports document types: client-api, faq, function-guide, overview, quick-start, release-note, run-demo.
version: 1.0.0
---

# ZEGO 文档结构设计技能

引导用户从头开始设计和编写符合 ZEGO 规范的技术文档。

## 适用场景

当用户需要创建新文档/大幅度重写现有文档（而非简单优化现有文档）时使用此技能。支持以下文档类型：

| 类型 | 用途 | 触发短语示例 |
|------|------|-------------|
| **overview** | 产品概述 | "写一个产品介绍" |
| **quick-start** | 快速开始指南 | "写快速开始文档" |
| **function-guide** | 功能指南 | "写功能使用指南" |
| **client-api** | 客户端 API 文档 | "写客户端 API 文档" |
| **run-demo** | 跑通示例代码 | "写示例代码使用说明" |
| **faq** | 常见问题 | "写 FAQ 文档" |
| **release-note** | 发布日志 | "写发布日志" |

## 工作流程

### Step 1: 确定文档类型

询问用户要创建的文档类型：

```
请确认要创建的文档类型：
1. overview - 产品概述（产品介绍、核心功能、应用场景、架构）
2. quick-start - 快速开始（5分钟上手指南）
3. function-guide - 功能指南（详细功能使用说明）
4. client-api - 客户端 API（接口文档）
5. run-demo - 跑通示例代码（Demo 运行指南）
6. faq - 常见问题（Q&A 形式）
7. release-note - 发布日志（版本更新说明）
```

### Step 2: 读取对应规范

根据文档类型，读取 `references/` 目录下对应的规范文件：

- **overview** → `references/overview.md`
- **quick-start** → `references/quick-start.md`
- **function-guide** → `references/function-guide.md`
- **client-api** → `references/client-api.md`
- **run-demo** → `references/run-demo.md`
- **faq** → `references/faq.md`
- **release-note** → `references/release-note.md`

### Step 3: 收集内容需求

根据规范文件中的必需章节，询问用户收集必要信息：

**Overview 类型示例问题：**
```
请提供以下信息：
1. 产品简介：这个产品是什么？解决什么问题？
2. 核心功能：列举主要功能特性
3. 应用场景：典型使用场景有哪些？
4. 产品架构：是否有架构图？需要说明哪些组件？
5. 计费说明：计费模式是什么？
```

### Step 4: 生成文档大纲

根据收集的信息和规范要求，生成文档大纲供用户确认：

```markdown
## 文档大纲预览

### 1. 产品简介
- [待填写：产品定义和价值主张]

### 2. 核心功能
- [待填写：功能列表]

### 3. 应用场景
- [待填写：场景描述]

...

请确认大纲结构是否符合预期，或提供修改意见。
```

### Step 5: 编写文档内容

用户确认大纲后，按以下原则编写文档：

**写作原则：**
1. **用户视角** - 从用户角度出发，说明"能做什么"而非"是什么"
2. **结构清晰** - 使用标题层级分明，段落简短
3. **代码示例** - 功能类文档必须包含可运行的代码示例
4. **图文并茂** - 复杂概念配合图示说明
5. **敬语规范** - 使用"您"而非"你"

**MDX 格式要求：**
- 使用标准 Markdown 语法
- 代码块指定语言类型
- 链接使用相对路径

### Step 6: 输出与确认

输出完整文档，询问用户是否需要调整：

```
文档已生成，请确认：
1. 结构是否完整？
2. 内容是否准确？
3. 是否需要补充或修改？
```

## 参考资源

### Reference Files

详细规范文件位于 `references/` 目录：

- **`references/overview.md`** - 产品概述结构标准
- **`references/quick-start.md`** - 快速开始结构标准
- **`references/function-guide.md`** - 功能指南结构标准
- **`references/client-api.md`** - 客户端 API 结构标准
- **`references/run-demo.md`** - 跑通示例代码结构标准
- **`references/faq.md`** - 常见问题结构标准
- **`references/release-note.md`** - 发布日志结构标准

## 使用示例

**场景：创建产品概述**

```
用户: 帮我写一个 AI 数字人的产品概述文档

Claude:
1. 确认文档类型为 overview
2. 读取 references/overview.md 规范
3. 询问产品简介、核心功能、应用场景等信息
4. 生成大纲供确认
5. 编写完整文档
6. 输出并等待反馈
```

## 注意事项

1. **严格遵循结构** - 每种文档类型都有必需章节，不可遗漏
2. **内容质量优先** - 宁可多问细节，不写模糊内容
3. **代码可运行** - 代码示例必须完整、可运行
4. **链接有效** - 所有内部链接必须指向存在的文档
5. **格式规范** - 遵循 ZEGO 文档的 MDX 格式要求
