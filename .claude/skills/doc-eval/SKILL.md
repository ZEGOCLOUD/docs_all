---
name: doc-eval
description: "This skill should be used when the user wants to evaluate documentation quality from multiple perspectives. Triggers on: Review 文档、评测文档、评估文档、doc eval、文档评价、文档质量、文档评测。"
version: 1.2.0
---

# 文档质量多角色评测

从不同用户角色视角评价技术文档质量，生成评分和改进建议。默认先输出本地 Markdown 产物，并将最终报告写入飞书；如果用户或调用方明确要求只输出本地 Markdown，则不写飞书。

## 核心原则

- **文档类型决定参与角色**。不是所有角色都该评测所有文档。CTO 去客户端 API 文档里找计费模式是文档类型定位错误，不是文档质量问题。详见 `references/rubric.md` 的匹配矩阵。
- **开发者统一按"零经验开发者"定位**：没有任何 ZEGO 产品经验（RTC、IM、AI Agent、数字人等均未使用过），不熟悉实时通讯行业概念，依赖文档解释一切术语和概念。

## 评测执行细则

具体阅读规则、零经验开发者定位、MDX 复用处理、链接跟随、术语检查、准确性判断和问题写作要求见 `references/evaluation-execution.md`。

执行角色评测的 subagent 必须读取该文件。

## 评测维度

6 个评测维度，详细评分标准见 `references/rubric.md`：

1. **信息架构** — 章节逻辑、顺序、层次
2. **内容完整性** — 该角色需要的信息是否齐全
3. **前提条件** — 前置要求是否明确
4. **参数/配置说明** — 参数含义、默认值、示例是否充分
5. **可发现性** — 能否快速找到所需内容
6. **准确性** — 信息是否与实际一致，有无过时内容。准确性判断细则见 `references/evaluation-execution.md`。

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

- **文档路径**: 要评测的一个或多个文档文件/目录路径
- **产品名称**: 产品名（跟文档路径至少填一个）
- **目标平台**: 要评测哪个平台的文档（如 Web、Android、iOS、Flutter、React Native、Electron 等）
- **测试范围**: 文档范围或功能范围（如快速开始、某个功能点、指定文档集合）
- **运行日期**: 默认使用当前日期，格式 `YYYY-MM-DD`
- **飞书写入模式**:
  - `standalone-default`: `doc-eval` 独立运行，默认写飞书
  - `local-only`: 用户或调用方明确要求不写飞书，只输出本地 Markdown

**run-name** 固定格式：

```text
{product}-{platform}-{scope}-{date}
```

报告输出目录：

```text
doc-test-reports/{run-name}/doc-eval/
```

### 2. 识别文档类型并匹配角色

1. **识别文档类型**：根据目录名判断文档属于哪种类型（产品概述、快速开始、客户端API、服务端API、FAQ 等）。类型列表见 `references/rubric.md` 的文档类型定义表。

2. **查匹配矩阵**：在 `references/rubric.md` 的「文档类型 × 角色匹配矩阵」中查找该文档类型对应哪些角色。

3. **确定参与角色**：
   - ⭐⭐⭐ 的角色必须评测
   - ⭐⭐ 的角色应评测
   - ⭐ 的角色可选（向用户确认）
   - ❌ 的角色跳过

4. **告知用户**：展示匹配结果，让用户确认参与角色。例如："这是快速开始文档，匹配到的角色是：客户端开发(⭐⭐⭐)、服务端开发(⭐⭐⭐)、全栈开发(⭐⭐⭐)、CTO(⭐⭐)、ZEGO技术支持(⭐⭐)。产品经理和计费说明不匹配，不参与评测。"

### 3. 准备本地产物目录

创建本地报告目录：

```text
doc-test-reports/{run-name}/doc-eval/
```

阶段至少输出：

```text
doc-test-reports/{run-name}/doc-eval/doc-eval-summary.md
doc-test-reports/{run-name}/doc-eval/role-*.md
```

`run-index.md` 如存在，由调用方维护；`doc-eval` 不负责更新总索引。

### 4. 执行评测并输出本地 Markdown（在 subagent 中执行）

使用 Agent 工具启动 subagent，在独立上下文中完成角色评测和本地 Markdown 写入。**所有角色报告和汇总报告的完整文本不返回主会话**，只返回摘要文件路径、报告路径、综合评分和必要的飞书链接。

**调用方式**：使用 Agent 工具，参数如下：
- `subagent_type`: `"general-purpose"`
- 每个需要评测的角色，启动一个对应的 `general-purpose` agent 处理。多个角色并行。
- `prompt`: 告知 subagent 执行以下评测流程：

**Subagent 内部流程**：

#### 4a. 按不同角色要求进行评测

1. 读取对应的角色定义文件（`references/role-*.md`）
2. 读取评分标准（`references/rubric.md`）
3. 读取评测执行细则（`references/evaluation-execution.md`）和报告格式（`references/report-templates-role.md`），按角色关注路径完整阅读目标文档并生成评测报告
4. **按文档类型校准评判标准**：注意“按文档类型评判”规则。（比如：不在快速开始文档里期待计费说明）
5. 逐维度评分并输出到角色报告文件

每个 agent 的 prompt 应包含：评测目标（文档路径列表、产品名称、目标平台、测试范围、文档类型、run-name、报告目录）和上述步骤指令。具体评测细节不要重复写在 prompt 中，要求 subagent 读取并遵循 `references/evaluation-execution.md` 和 `references/report-templates-role.md`。

每个 agent 还需在评测报告末尾生成**集成验证输入（可选）**，包括：
- 建议构建验证关注点（按角色阅读路径提炼）
- 可能阻塞构建验证的问题（🔴 问题汇总）
- 需要用户准备的信息（账号、密钥、环境等）

#### 4b. 写入角色报告本地文件

每个角色评测完成后，写入：

```text
doc-test-reports/{run-name}/doc-eval/role-{role-id}.md
```

不要把完整角色报告返回主会话。

#### 4c. 生成汇总报告本地文件

所有角色报告都完成后，启动一个 `general-purpose` agent 生成汇总报告。该 agent：

1. 读取汇总分析方法（`references/role-report.md`）
2. 读取汇总报告格式（`references/report-templates.md`）
3. 读取本地角色报告文件：`doc-test-reports/{run-name}/doc-eval/role-*.md`
4. 交叉对比各角色的评分和发现
5. 识别共性问题、按优先级排序改进建议
6. 生成汇总报告：`doc-test-reports/{run-name}/doc-eval/doc-eval-summary.md`

不要把所有角色完整报告塞进 prompt 或返回主会话；汇总 agent 必须从本地文件读取角色报告。

#### 4d. 按需写入飞书

飞书写入策略：

| 模式 | 是否写飞书 | 说明 |
|------|------------|------|
| `standalone-default` | 是 | 默认就写入 |
| `local-only` | 否 | 用户或调用方明确要求不写飞书 |

仅当需要写飞书时，读取 `references/feishu-write.md` 并按其中说明创建飞书文件夹、写入角色报告和汇总报告。

#### 4e. Subagent 最终返回给主会话的信息

仅返回以下内容，不返回完整报告文本：

```markdown
## Result

- status: completed / failed / blocked
- summary_file: doc-test-reports/{run-name}/doc-eval/doc-eval-summary.md
- detail_files:
  - doc-test-reports/{run-name}/doc-eval/role-client-dev.md
  - doc-test-reports/{run-name}/doc-eval/role-fullstack-dev.md
- document_link: {飞书汇总报告链接或本地 doc-eval-summary.md 路径}
- summary: 综合评分 X/5，发现 N 个问题，其中 M 个阻塞
- next_action: continue / stop / needs_user_input
```

如果已写飞书，可额外返回：

- 飞书任务文件夹链接
- 各角色评测报告飞书链接
- 汇总报告飞书链接

**Subagent 完成后验证**：
- ✅ `doc-eval-summary.md` 已生成
- ✅ 参与角色的 `role-*.md` 已生成
- ✅ 综合评分已返回
- ✅ 如果执行了飞书写入，飞书链接列表已返回
- ❌ 如果 subagent 失败或未返回本地文件路径，提示用户检查

**注意**：subagent 在独立上下文中运行，主会话不保留角色报告和汇总报告的详细内容。所有评测结果通过本地 Markdown 文件保存；飞书只是独立运行时的默认发布目标。

### 5. 输出结果

向用户展示：
- 本地报告目录：`doc-test-reports/{run-name}/doc-eval/`
- 文档评测摘要：`doc-test-reports/{run-name}/doc-eval/doc-eval-summary.md`
- 各角色报告路径
- 综合评分一句话总结
- 如果已写飞书，展示飞书任务文件夹、各角色报告和汇总报告链接

## 参考资源

| 文件 | 用途 |
|------|------|
| `references/rubric.md` | 文档类型定义、角色匹配矩阵、评分标准、权重表、校准规则 |
| `references/evaluation-execution.md` | subagent 执行评测时使用的阅读、链接、复用、术语、定位和问题写作细则 |
| `references/feishu-write.md` | 需要写入飞书时使用的创建文件夹和写入文档说明 |
| `references/role-cto.md` | CTO 角色画像、阅读路径、评分注意事项 |
| `references/role-support.md` | ZEGO技术支持画像、阅读路径、评分注意事项 |
| `references/role-client-dev.md` | 客户端开发画像、阅读路径、评分注意事项 |
| `references/role-server-dev.md` | 服务端开发画像、阅读路径、评分注意事项 |
| `references/role-fullstack-dev.md` | 全栈开发画像、阅读路径、评分注意事项 |
| `references/role-report.md` | 汇总分析方法、交叉分析维度、优先级排序 |
| `references/report-templates-role.md` | 角色报告输出格式 |
| `references/report-templates.md` | 汇总报告输出格式 |

## 关联 Skills

| Skill | 用途 |
|-------|------|
| `url-to-mdx` | 将文档 URL path（如 `/real-time-video-web/...`）解析为本地 MDX 文件 |
| `api-short-link-to-mdx` | 将 API `@` 短链（如 `@startPublishingStream`）解析为本地 API 参考 MDX 文件 |
