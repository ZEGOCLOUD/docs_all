---
name: make-integration-test
description: >
  This skill should be used when the user wants to run a full "集成测试" (integration test) pipeline —
  document quality evaluation followed by integration testing (build, compile, verify). This skill
  chains two phases: (1) multi-role document evaluation with reports written to Feishu, and
  (2) simulating a zero-experience developer following the documentation to build, compile, and
  test a project.

  Triggers on: "集成测试", "运行集成测试", "make-integration-test", "integration test",
  "run integration test", "文档集成测试", "接入测试", or when the user explicitly asks to both
  evaluate docs AND test integration.

  Do NOT trigger when the user only wants document evaluation (use doc-eval skill instead),
  or only wants to create code examples (use example-code-creator agent instead).
version: 1.0.0
---

# 接入测试全流程

编排完整的"接入测试"流程：从多角色文档质量评测到模拟零经验开发者实际构建验证。发现文档在真实接入场景中的所有问题。

## 核心人设

**零经验开发者**：没有任何 ZEGO 产品经验，不熟悉实时通讯概念（RTC、IM、房间、Token、鉴权等），完全依赖文档指导每一步操作。不会猜测行业惯例，不会主动翻源码。

**严格文档执行者**：只做文档描述的事情，不补充文档未提及的步骤。如果文档没说要做某件事，就不做。

**从文档推断一切**：目标平台、依赖版本、构建命令全部从文档内容识别，不预设任何前提。

## 依赖资源

### Skills

| Skill | 用途 | 调用时机 |
|-------|------|---------|
| `doc-eval` | 文档评测（评分标准、角色定义、输出格式） | Step 2（文档评测） |
| `create-integration-demo` | 模拟零经验开发者构建验证（识别平台→模拟阅读→收集凭证→构建→写代码→编译→记录问题） | Step 4（集成测试构建阶段） |
| `auto-test-demo` | 测试 demo 项目（设计用例、执行测试、截图） | Step 5（自动化测试阶段） |

### 参考文件

| 文件 | 用途 |
|------|------|
| `references/feishu-operations.md` | 飞书文档创建、写入、文件夹操作规范 |
| `references/report-templates.md` | 集成测试报告模板（含详细步骤格式、类别标记说明、问题定位规范）和汇总报告重写模板 |

### 脚本

| 脚本 | 用途 |
|------|------|
| `scripts/doc-link.sh` | 将工作区文件路径+行号转换为 GitHub 可跳转链接。用法：`bash .claude/skills/make-integration-test/scripts/doc-link.sh <相对路径> [<行号>]` |

### 工具

- **飞书文档操作**: `lark-cli` 命令行工具

## 工作流程

```
Step 1: 收集参数
Step 2: 按 doc-eval skill 指引执行文档多角色评测
Step 3: 确认评测输出完整，记录飞书文件夹 node_token
Step 4: 调用 create-integration-demo skill 执行构建验证
Step 5: 调用 auto-test-demo skill 完成自动化测试
Step 6: 生成集成测试报告并追加到飞书
Step 7: 根据集成测试结果重写文档质量评测汇总报告
Step 8: 展示最终结果
```

### Step 1: 收集参数

使用 AskUserQuestion 确认以下信息（用户可能已提供部分信息，只补充缺失项）：

1. **产品名称** — 要测试哪个产品（如 AIAgent、实时音视频、即时通讯、数字人等）
2. **目标平台** — 测试哪个平台（如 Web、Android、iOS、Flutter、React Native、uni-app、Electron 等）
3. **测试范围** — 具体测试什么内容：
   - 快速开始（端到端完整接入流程）
   - 某个具体功能点（如屏幕共享、美颜、录制等）
   - 指定的文档路径（MDX 文件路径）

如果用户提供了文档路径，从文档路径和内容中推断产品名称、平台和功能范围。

**输出目录**：项目代码和测试文件统一放在 workspace 根目录下的 `examples/` 目录中，命名格式为 `examples/{产品名}-{平台}-integration-test/`（如 `examples/aiagent-web-integration-test/`）。

### Step 2: 执行文档多角色评测

按照 `doc-eval` skill 的完整指引和步骤执行文档多角色评测。调用 `doc-eval` skill 后严格遵循其编排流程（识别文档类型、匹配角色、创建飞书文件夹、并行评测、写报告、汇总）。

### Step 3: 确认评测输出

doc-eval 完成后，确认以下输出已就绪：
- ✅ 飞书任务文件夹已创建，记录 `node_token`
- ✅ 各角色评测报告已写入飞书
- ✅ 汇总报告已写入飞书
- ✅ 综合评分和关键问题已记录

如果 doc-eval 未能完成所有输出，补充完成后再继续。

### Step 4: 构建验证（调用 create-integration-demo skill）

调用 `create-integration-demo` skill，传入文档路径、产品名称、输出目录。该 skill 完整执行：
1. 识别目标平台
2. 模拟零经验开发者阅读路径
3. 收集运行所需的账号和密钥（向用户确认）
4. 构建项目
5. 编写代码
6. 编译验证
7. 记录所有问题（含 5 类归类）

skill 完成后，获取：构建结果、问题列表（含归类和严重度）。

### Step 5: 自动化测试（调用 auto-test-demo skill，禁止跳过此步骤）

调用 `auto-test-demo` skill，传入项目路径和识别的平台。该 skill 完整执行：
1. 分析项目代码，设计测试用例
2. 生成 test-cases.md 和 test-cases.sh
3. 用户确认测试用例
4. 执行测试
5. 截图

传入参数：项目路径（`examples/{产品名}-{平台}-integration-test/`）、识别的平台。

skill 完成后，获取自动化测试报告
如果自动化测试报告发现非文档指引问题(实现问题)，可以尝试修复后再重新进行自动化测试。最多尝试3轮。

---

### Step 6: 生成集成测试报告并追加到飞书

将步骤 4 和步骤 5 的构建结果、问题列表、自动化测试报告合并作为集成测试报告数据来源，**缺一不可**。

在 Step 2 创建的飞书文件夹下创建集成测试报告文档。报告格式见 `references/report-templates.md` 的「集成测试报告」模板。

报告关键要求：
- **步骤详细化**：每个步骤必须包含定位（用 `scripts/doc-link.sh` 生成 GitHub 链接）、原文内容摘录、执行操作、结果、以及问题项（为什么是问题、改进建议、问题归类）
- **类别标记**：必须使用文字+图标（如 `📄 文档问题` 而非仅 `📄`）
- **自动化测试结果**：直接嵌入 auto-test-demo 生成的 `test-report.md` 完整内容，不重新组织

飞书操作规范见 `references/feishu-operations.md`。关键要点：
- 先用 `docs +create` 创建文档，再用 `docs +update --command overwrite` 写入完整内容
- `--content` 用 heredoc 包裹字符串，不能用文件路径
- overwrite 内容的第一行必须是 `# 标题`

注意：要把示例代码（清理构建、依赖和敏感信息后）和自动化测试报告压缩成一个zip包用 lark-cli 上传到【集成测试报告】文档。截图则直接插入到【集成测试报告】文档的自动化测试报告章节下。

### Step 7: 根据集成测试结果重写文档质量评测汇总报告

集成测试完成后，回到 Step 2 生成的文档质量评测汇总报告，结合集成测试的实际验证结果重新梳理并覆盖写入。

**核心逻辑**：文档评测是"纸上分析"，集成测试是"实际验证"。汇总报告必须融合两者的发现，才能全面反映文档的真实质量。

**重写内容**（在原汇总报告基础上增补）：

1. **问题验证结果** — 每个文档评测发现的问题，标注集成测试的实际验证结果：
   - ✅ 确认阻塞：文档评测发现的🔴问题，集成测试确实复现
   - ⚠️ 部分阻塞：问题描述属实但影响范围比预期小
   - ❌ 未阻塞：文档评测判断为问题，但实际操作中可以绕过或不影响
   - 🆕 集成测试独有发现：文档评测未发现，但实际操作中暴露的问题

2. **问题严重度重新评定** — 根据集成测试的实际验证，调整部分问题的严重度：
   - 文档评测认为是🔴但实际未阻塞的 → 降级为🟡
   - 文档评测认为是🟡但实际导致阻塞的 → 升级为🔴

3. **问题归类补充** — 文档评测用 6 维度评分，集成测试用 5 类别归类。将两种视角合并：
   - 每个问题同时标注文档评测维度评分和集成测试问题类别（📄 文档问题 / 🔧 代码实现问题 / 🏗️ 环境问题 / 🔗 链接问题 / 📖 概念缺失）

4. **综合评分调整** — 如果集成测试发现的问题数量和严重度与文档评测差异较大，在汇总报告中说明是否建议调整综合评分

5. **最终改进建议** — 合并两个阶段的建议，去重并按真实优先级（经集成测试验证后的）重新排序

**写入飞书**：使用 `docs +update --command overwrite` 覆盖原汇总报告文档，内容第一行必须是 `# 标题`。

### Step 8: 展示最终结果

向用户展示完整结果：

1. **飞书文件夹链接**（包含所有报告）
2. **第一阶段结果**:
   - 文档评测综合评分 X/5
   - 各角色报告链接
   - 汇总报告链接
3. **第二阶段结果**:
   - 集成测试报告链接
   - 问题归类统计（5 类各多少）
   - 关键阻塞问题清单
4. **一句话总结**: "文档综合评分 X/5，集成测试发现 N 个问题（🔴 M 个阻塞），主要问题集中在 [类别]。"

## 执行原则

1. **Step 2 完全遵循 doc-eval skill 的指引**，不在本 skill 中重复其步骤
2. **Step 4 完全遵循 create-integration-demo skill 的指引**，不在本 skill 中重复其步骤
3. **Step 5 完全遵循 auto-test-demo skill 的指引**，不在本 skill 中重复其步骤
4. **确认每步输出完整后再进入下一步**
5. **使用 TaskCreate / TaskUpdate 跟踪每个步骤的进度**
6. **飞书文档操作遵循 `references/feishu-operations.md` 规范**
