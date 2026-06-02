---
name: doc-eval
description: "This skill should be used when the user wants to evaluate documentation quality from multiple perspectives. Triggers on: Review 文档、评测文档、评估文档、doc eval、文档评价、文档质量、文档评测。"
version: 1.1.0
---

# 文档质量多角色评测

从不同用户角色视角评价技术文档质量，生成评分和改进建议，结果输出到飞书文档。

## 核心原则

**文档类型决定参与角色**。不是所有角色都该评测所有文档。CTO 去客户端 API 文档里找计费模式是文档类型定位错误，不是文档质量问题。详见 `references/rubric.md` 的匹配矩阵。

**开发者统一按"零经验开发者"定位**：没有任何 ZEGO 产品经验（RTC、IM、AI Agent、数字人等均未使用过），不熟悉实时通讯行业概念，依赖文档解释一切术语和概念。

## 零经验开发者定位

所有开发者角色统一按"零经验开发者"定位：
- **没有任何 ZEGO 产品经验**（RTC、IM、AI Agent、数字人等均未使用过）
- **不熟悉实时通讯行业概念**（如房间、用户 ID、Token、鉴权、回调等）
- **依赖文档解释一切术语和概念**
- **不会猜测或假设行业惯例**
- **了解自己角色应知技术**（如Android开发知道怎么用Android Studio创建项目，Web开发知道有npm、pnpm等包管理器可以安装依赖）

这意味着：文档必须解释所有 ZEGO 特有概念和行业术语，不能假设读者已知。

## 术语检查原则

**动态识别，不依赖硬编码列表**

各角色评测时动态识别文档中的术语，检查文档是否解释：
1. 任何技术名词（如 SDK、API、Token、回调、鉴权）
2. 任何 ZEGO 特有概念（如房间、StreamID、用户 ID）
3. 任何行业特定术语（如推流、拉流、连麦）

**判断标准**：
- 文档是否首次出现该术语时提供解释
- 解释是否清晰（能理解的文字描述，不是"就是xxx"）
- 示例是否充分（代码示例、参数说明、返回值说明）

**不要求解释的内容**：
- 编程语言基础概念（如变量、函数、类）
- Web/移动端通用概念（如 HTTP、JSON、Promise）

## 文档复用语法说明

文档中广泛使用跨平台内容复用机制，目的是保持多平台内容同步、降低维护成本。**这是正常的设计模式，不得将其评价为文档问题。**

### 复用语法

**导入并渲染：**
```mdx
import Content from '/core_products/aiagent/zh/android/quick-start.mdx'

<Content platform="Web"/>
```

**源文件中的条件渲染：**
```mdx
这段内容所有平台都会展示。

:::if{props.platform="Web"}
这段内容仅在 platform="Web" 时展示。
:::

:::if{props.platform="Android"}
这段内容仅在 platform="Android" 时展示。
:::
```

### 评测时的处理方式

1. **识别复用关系**：当文档包含 `import ... from '...'` 和 `<Content .../>` 时，说明该文档复用了另一个源文件
2. **跟踪读取源文件**：必须读取 import 指向的源文件，不能只看当前文件
3. **拼合完整内容**：将源文件中无条件渲染的内容 + 匹配当前平台条件的条件渲染内容，视为当前文档的完整内容
4. **不评判语法本身**：不得将 `import`、`:::if{...}`、`props.platform` 等复用语法标记为"内容缺失"、"格式混乱"或"结构不清晰"

### 常见误判场景（必须避免）

| 误判 | 正确理解 |
|------|----------|
| "文档只有 import 语句，缺少实际内容" | 文档通过 import 复用了源文件的完整内容 |
| "出现 :::if{...} 语法，影响阅读" | 这是条件渲染指令，最终渲染时只显示匹配条件的内容 |
| "某个平台的操作步骤在本文档中找不到" | 可能是条件渲染内容，需检查源文件 |
| "出现 `[sendSEI](@sendSEI)` 这样的无效链接" | 这是 ZEGO 文档的 API 短链接语法，由文档系统自动解析为可跳转的 API 文档链接，不是错误 |
| "示例代码 `let appID = ;` 语法错误" | 这是故意的占位写法，让程序报错防止用户忘记填写。重点检查是否有注释说明如何获取该值，有注释说明则可接受，无注释说明则是文档问题 |

## 评测维度

6 个评测维度，详细评分标准见 `references/rubric.md`：

1. **信息架构** — 章节逻辑、顺序、层次
2. **内容完整性** — 该角色需要的信息是否齐全
3. **前提条件** — 前置要求是否明确
4. **参数/配置说明** — 参数含义、默认值、示例是否充分
5. **可发现性** — 能否快速找到所需内容
6. **准确性** — 信息是否与实际一致，有无过时内容。**禁止编造**：只能对照文档实际写的内容判断对错。不能把自己从外部知识引入的技术细节当作"文档应该说的"来评判。如果文档没提到某个技术细节（如加密算法），不能说"文档说的加密方式不对"——因为文档根本没说。只能评判文档**实际写了的内容**是否正确。

## 问题严重程度

| 级别 | 标记 | 含义 |
|------|------|------|
| 阻塞 | 🔴 | 导致该角色无法完成目标，必须修复 |
| 体验差 | 🟡 | 可以完成但体验糟糕，建议修复 |
| 优化建议 | 🟢 | 锦上添花，可选择性改进 |

## 角色

各角色的关注路径、模拟问题、评分权重详见 `references/rubric.md`。

| 角色 | 目标 | 评分侧重 |
|------|------|----------|
| CTO / 技术决策者 | 评估产品是否满足业务需求 | 信息架构 > 内容完整性 > 准确性 |
| 产品经理 | 评估产品功能、定位、计费 | 内容完整性 > 信息架构 > 准确性 |
| ZEGO技术支持 | 用文档帮用户解答问题 | 内容完整性 > 准确性 > 参数/配置说明 |
| 客户端开发 | 按文档集成客户端 SDK | 参数/配置说明 > 内容完整性 > 前提条件 |
| 服务端开发 | 按文档集成服务端 | 参数/配置说明 > 内容完整性 > 前提条件 |
| 全栈开发 | 按文档集成客户端+服务端 | 参数/配置说明 > 内容完整性 > 前提条件 |

角色画像和阅读路径见对应文件：`references/role-cto.md`、`references/role-support.md`、`references/role-client-dev.md`、`references/role-server-dev.md`、`references/role-fullstack-dev.md` 等。

## 编排流程

当用户要求评测文档时，按以下流程执行：

### 1. 收集参数

确认以下信息（用户可能已提供，未提供的用 AskUserQuestion 补充）：

- **文档路径**: 要评测的文档文件或目录路径
- **产品名称**: 产品名

### 2. 识别文档类型并匹配角色

1. **识别文档类型**：根据目录名判断文档属于哪种类型（产品概述、快速开始、客户端API、服务端API、FAQ 等）。类型列表见 `references/rubric.md` 的文档类型定义表。

2. **查匹配矩阵**：在 `references/rubric.md` 的「文档类型 × 角色匹配矩阵」中查找该文档类型对应哪些角色。

3. **确定参与角色**：
   - ⭐⭐⭐ 的角色必须评测
   - ⭐⭐ 的角色应评测
   - ⭐ 的角色可选（向用户确认）
   - ❌ 的角色跳过

4. **告知用户**：展示匹配结果，让用户确认参与角色。例如："这是快速开始文档，匹配到的角色是：客户端开发(⭐⭐⭐)、服务端开发(⭐⭐⭐)、全栈开发(⭐⭐⭐)、CTO(⭐⭐)、ZEGO技术支持(⭐⭐)。产品经理和计费说明不匹配，不参与评测。"

### 3. 创建飞书任务文件夹

在飞书知识库的「接入测试」节点下创建本次评测的文件夹。

父节点信息：
- space_id: `7187666870011232257`
- parent_node_token: `Bvy6wsTvjiLh7bkzOxVcwvyunTH`

```bash
lark-cli wiki nodes create --params '{"space_id":"7187666870011232257"}' --data '{"parent_node_token":"Bvy6wsTvjiLh7bkzOxVcwvyunTH","node_type":"origin","obj_type":"docx","title":"【YY-MM-DD 产品名-文档类型 接入测试】"}' --as user
```

注意：`space_id` 是 path 参数，必须用 `--params` 传；body 参数用 `--data` 传。两者分开。

记录返回的 node_token，后续文档都在这个节点下创建。

### 4. 并行启动角色评测

并行启动匹配到的 `general-purpose` agent，每个 agent：

1. 读取对应的角色定义文件（`references/role-*.md`）
2. 读取评分标准（`references/rubric.md`）
3. 读取报告格式（`references/output-format-role.md`）
4. 完整阅读目标文档：
   - **跟踪 MDX import**：遇到 `import Content from '/path/to/file.mdx'` + `<Content platform="xxx"/>` 时，必须读取源文件
   - **拼合完整内容**：源文件中无条件渲染的内容 + 匹配当前 `platform` 条件的 `:::if{props.platform="xxx"}` 内容，构成当前文档的完整有效内容
   - **不评判复用语法**：import 语句和 `:::if{...}` 条件渲染指令是正常的内容复用机制，不得将其标记为文档问题
   - **跟随文档内所有链接**：文档中的链接是文档内容的一部分，必须跟随读取后才能判断信息是否缺失。不得声称"文档没有提供链接"或"文档没有说明 X"，除非实际跟随了链接并确认目标内容确实不包含所需信息。

     | 链接格式 | 示例 | 处理方式 |
     |----------|------|---------|
     | @ 短链 | `[sendSEI](@sendSEI)` | 用 `api-short-link-to-mdx` skill 解析到本地 API MDX 文件，读取 API 说明 |
     | 相对路径 | `[快速开始](../02-Quick%20start.mdx)` | 基于当前 MDX 文件路径解析为本地文件路径，直接读取 |
     | URL path | `[Token 鉴权](/real-time-video-web/communication/using-token-authentication)` | 用 `url-to-mdx` skill 解析到本地 MDX 文件并读取 |
     | 完整 URL | `https://doc-zh.zego.im/...` | 用 `url-to-mdx` 尝试解析到本地文件；无法解析则用 Web 工具读取 |
     | 页内锚点 | `#signature-sample-code` | 在当前文档中查找对应标题即可 |

     **允许批评的角度**：
     - 链接放置位置不明显（关键信息藏在不显眼的小字链接中）
     - 需要跳转超过 2 层才能找到关键操作信息（信息过于分散）
     - 链接文字不够描述性（如用"这里"而非"Token 鉴权指南"）

     **不允许**：声称"没有提供链接"或"没有说明"——如果文档有链接但 agent 没跟，这是 agent 的问题。
5. 按角色的 Phase 1-6 走查
6. **按文档类型校准评判标准**：注意"按文档类型评判"规则，不在快速开始文档里期待计费说明
7. 逐维度评分并生成评测报告

每个 agent 的 prompt 应包含：评测目标（文档路径、产品名称、文档类型）和上述步骤指令。重点强调：**每个问题必须具体定位到文件和行号，必须引用原文，必须从角色视角解释为什么是问题，改进建议必须可操作（给出建议文案）。** 详见 `references/output-format-role.md` 的"关键要求"部分。

每个 agent 还需在评测报告末尾生成**集成测试简报**，包括：
- 预期测试步骤（按角色阅读路径提炼的关键步骤）
- 发现的阻塞点（🔴 问题汇总）
- 环境前置条件（需要准备的账号、密钥、环境）

### 5. 将角色报告写入飞书

每个角色评测完成后，立即将报告写入飞书文档。分两步：

**Step A: 创建空文档**（在任务文件夹下创建）
```bash
lark-cli docs +create --api-version v2 --parent-token {folder_node_token} --doc-format markdown --content "$(cat <<'EOF'
# 【角色名】评测报告
EOF
)"
```

**Step B: 用 overwrite 写入完整内容**（`--content` 接收字符串，不是文件路径）
```bash
lark-cli docs +update --api-version v2 --doc {document_id} --command overwrite --doc-format markdown --content "$(cat <<'EOF'
# 【角色名】评测报告
... 完整报告 markdown 内容 ...
EOF
)"
```

关键注意事项：
- `--content` 直接接收字符串内容，**不能**用 `@-`（stdin）或 `@file.md`（文件路径）
- 内容较长时用 `$(cat <<'EOF' ... EOF)` heredoc 包裹
- `docs +create` 的 `--content` 参数必填，不能为空
- 长文档可先 `+create` 建骨架，再用 `+update --command append` 分段追加
- **文档标题从内容中的 `#`（h1）提取**：`+update --command overwrite` 会替换全部内容，如果新内容没有 `#` 标题（比如用了 `##`），文档标题会变成 "Untitled"。确保 overwrite 的内容第一行是 `# 标题`

### 6. 生成汇总报告

所有角色报告都完成后，启动一个 `general-purpose` agent 生成汇总报告。该 agent：

1. 读取汇总分析方法（`references/role-report.md`）
2. 读取汇总报告格式（`references/output-format-report.md`）
3. 交叉对比各角色的评分和发现
4. 识别共性问题、按优先级排序改进建议
5. 生成汇总报告

prompt 中需包含所有角色的完整评测结果。

### 7. 将汇总报告写入飞书

同 Step 5 的方式：先用 `docs +create` 创建文档，再用 `docs +update --command overwrite` 写入完整汇总内容。

### 8. 输出结果

向用户展示：
- 任务文件夹飞书链接
- 各角色评测报告链接
- 汇总报告链接
- 综合评分一句话总结

### 9. 自动询问是否运行集成测试

所有报告完成后，自动向用户展示集成测试提示：

> 是否需要运行集成测试来验证这些问题？
>
> 集成测试会：
> - 模拟零经验开发者按文档操作
> - 实际构建项目、编写代码
> - 调用自动化测试技能验证功能
> - 生成问题归类报告（📄文档问题/🔧代码实现问题/🏗️环境问题/🔗链接问题/📖概念缺失）
>
> 输入 /doc-integration-test 开始，或跳过。

如果用户确认，调用 doc-integration-test 技能，传入：目标文档路径、产品名称、飞书任务文件夹 node_token。

## 输出格式

- 角色报告格式: `references/output-format-role.md`
- 汇总报告格式: `references/output-format-report.md`

## 参考资源

| 文件 | 用途 |
|------|------|
| `references/rubric.md` | 文档类型定义、角色匹配矩阵、评分标准、权重表、校准规则 |
| `references/role-cto.md` | CTO 角色画像、阅读路径、评分注意事项 |
| `references/role-support.md` | ZEGO技术支持画像、阅读路径、评分注意事项 |
| `references/role-client-dev.md` | 客户端开发画像、阅读路径、评分注意事项 |
| `references/role-server-dev.md` | 服务端开发画像、阅读路径、评分注意事项 |
| `references/role-fullstack-dev.md` | 全栈开发画像、阅读路径、评分注意事项 |
| `references/role-report.md` | 汇总分析方法、交叉分析维度、优先级排序 |
| `references/output-format-role.md` | 角色报告输出格式 |
| `references/output-format-report.md` | 汇总报告输出格式 |

## 工具脚本

| 文件 | 用途 |
|------|------|
| `scripts/doc-link.sh` | 将文件相对路径+行号转换为 GitHub 可跳转链接（飞书报告中使用） |

## 关联 Skills

| Skill | 用途 |
|-------|------|
| `url-to-mdx` | 将文档 URL path（如 `/real-time-video-web/...`）解析为本地 MDX 文件 |
| `api-short-link-to-mdx` | 将 API `@` 短链（如 `@startPublishingStream`）解析为本地 API 参考 MDX 文件 |
