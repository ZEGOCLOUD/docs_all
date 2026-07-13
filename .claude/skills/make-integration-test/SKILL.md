---
name: make-integration-test
description: >
  Use this skill when the user wants to run the full ZEGO documentation access-test workflow:
  documentation evaluation, demo construction, automated demo testing, final cross-stage synthesis,
  and optional Feishu publication. Triggers on: "集成测试", "接入测试", "文档接入测试",
  "make-integration-test", "integration test", "run full integration test", or when the user
  explicitly asks to both evaluate docs and verify a runnable integration demo. Do not use this
  skill when the user only wants doc evaluation, only wants to build a demo, or only wants to run
  tests; use the narrower skill directly in those cases.
version: 2.0.0
---

# 接入测试总控

执行完整接入测试流程：先生成本地阶段产物，再汇总校正，最后按需写入飞书。主会话只接收阶段结论、文件路径、阻塞状态和最终综合判断。

## 产物目录

报告产物写入仓库根目录：

```text
doc-test-reports/{run-name}/
  run-index.md
  doc-eval/
  build-verification/
  auto-test/
  examples/
    {demo-name}/
  build-test-report.md
  doc-eval-corrected/
  feishu-report-manifest.json
  feishu-report-links.md
```

示例代码写入：

```text
doc-test-reports/{run-name}/examples/{demo-name}/
```

`demo-name` 默认使用：

```text
{product}-{platform}-{scope}-demo
```

## 阶段状态

`run-index.md` 是总控维护的阶段索引。阶段开始、完成、失败、跳过时都要更新 `run-index.md`。

每次启动 subagent 时，prompt 都要包含本次任务简介和用户特殊要求，例如测试目标、文档范围、目标分支、SDK 或测试产物来源、必须覆盖的功能级别、账号/设备/环境要求、报告写法要求等。尽量保留用户原话中的关键短语，避免改写丢信息。

`run-index.md` 模板：

```markdown
# {run-name}

## 基本信息

| 字段 | 内容 |
|------|------|
| 产品 | {product} |
| 平台 | {platform} |
| 范围 | {scope} |
| 运行日期 | {date} |
| 目标文档 | {一个或多个文档路径/链接} |
| 示例项目 | doc-test-reports/{run-name}/examples/{demo-name}/ |

## 阶段状态

| 阶段 | 状态 | 摘要文件 | 文档链接 | 说明 |
|------|------|----------|----------|------|
| doc-eval | pending | doc-eval/doc-eval-summary.md | doc-eval/doc-eval-summary.md |  |
| build-verification | pending | build-verification/build-summary.md | build-verification/build-summary.md |  |
| auto-test | pending | auto-test/test-summary.md | auto-test/test-summary.md |  |
| report-publish | pending | feishu-report-links.md | feishu-report-links.md |  |
```

状态值使用：`pending`、`running`、`completed`、`failed`、`blocked`、`skipped`。`文档链接` 列初始写本地相对链接；写入飞书后，替换为对应飞书文档链接。

## 工作流程

### Step 1: 收集参数并初始化目录

确认用户已提供或可从文档路径推断以下信息：

- 产品名称
- 目标平台
- 测试范围
- 一个或多个目标文档路径
- 运行日期，默认当天，格式 `YYYY-MM-DD`
- 是否写入飞书，默认完整流程结束后写入；用户明确要求本地-only 时跳过飞书

生成 `run-name` 和 `demo-name`：

```text
run-name = {product}-{platform}-{scope}-{date}
demo-name = {product}-{platform}-{scope}-demo
```

创建：

```text
doc-test-reports/{run-name}/
doc-test-reports/{run-name}/doc-eval/
doc-test-reports/{run-name}/build-verification/
doc-test-reports/{run-name}/auto-test/
doc-test-reports/{run-name}/examples/{demo-name}/
```

初始化 `run-index.md`，将 `doc-eval` 置为 `running`。

注意：涉及飞书文档的读取等操作时，可根据 `lark-wiki`,`lark-drive`,`lark-doc` 几个 skill 指引进行操作。

### Step 2: 文档评测

启动独立 subagent，prompt 要求加载并使用 `doc-eval` skill，按该 skill 指引完成文档评测；不要在主会话 prompt 中写一套评测流程来替代它。传入：

- 本次任务简介和用户特殊要求
- 目标文档列表
- 产品、平台、范围、日期、`run-name`
- 输出目录：`doc-test-reports/{run-name}/doc-eval/`
- 飞书写入模式：`local-only`
- 固定句式：”加载 doc-eval skill 并按其指引完成文档评测“

要求 subagent 只返回：

```markdown
## Result

- status: completed / failed / blocked
- summary_file: doc-test-reports/{run-name}/doc-eval/doc-eval-summary.md
- detail_files:
  - doc-test-reports/{run-name}/doc-eval/role-*.md
- document_link: doc-eval/doc-eval-summary.md
- summary: 综合评分 X/5，发现 N 个问题，其中 M 个阻塞
- next_action: continue / stop / needs_user_input
```

完成后验证文件存在并更新 `run-index.md`。如果 `doc-eval` 阻塞，需要把原因写进 `run-index.md`，由用户决定是否继续后续构建验证。

### Step 3: 构建验证

将 `build-verification` 置为 `running`，启动独立 subagent，prompt 要求加载并使用 `create-integration-demo` skill，按该 skill 指引完成构建验证；不要在主会话 prompt 中写一套构建或代码实现流程来替代它。传入：

- 本次任务简介和用户特殊要求
- 目标文档列表
- 产品、平台、范围、日期、`run-name`、`demo-name`
- 示例项目目录：`doc-test-reports/{run-name}/examples/{demo-name}/`
- 报告目录：`doc-test-reports/{run-name}/build-verification/`
- 前置输入：`doc-test-reports/{run-name}/doc-eval/doc-eval-summary.md`
- doc-eval 阶段返回的关键结论
- 固定句式：”加载 create-integration-demo skill 并按其指引完成构建验证“

要求 subagent 只返回：

```markdown
## Result

- status: completed / failed / blocked
- summary_file: doc-test-reports/{run-name}/build-verification/build-summary.md
- detail_files:
  - doc-test-reports/{run-name}/build-verification/build-steps.md
  - doc-test-reports/{run-name}/build-verification/build-issues.md
- demo_dir: doc-test-reports/{run-name}/examples/{demo-name}/
- document_link: build-verification/build-summary.md
- summary: 构建是否成功，发现 N 个问题，其中 M 个阻塞
- next_action: continue / stop / needs_user_input
```

完成后验证报告和示例项目存在并更新 `run-index.md`。若构建没有得到可运行入口，将 `auto-test` 标记为 `skipped` 或 `blocked`，并直接进入最终综合。

### Step 4: 自动化测试

只有示例项目已经可编译或可运行时才执行。将 `auto-test` 置为 `running`，启动独立 subagent，prompt 要求加载并使用 `auto-test-demo` skill，按该 skill 指引完成自动化测试；不要在主会话 prompt 中写一套测试流程或测试用例清单来替代它。传入：

- 本次任务简介和用户特殊要求
- 项目目录：`doc-test-reports/{run-name}/examples/{demo-name}/`
- 平台、范围、`run-name`、`demo-name`
- 报告目录：`doc-test-reports/{run-name}/auto-test/`
- 前置报告：
  - `doc-test-reports/{run-name}/build-verification/build-summary.md`
  - `doc-test-reports/{run-name}/build-verification/build-issues.md`
- build-verification 阶段返回的关键结论，包括示例项目入口、运行方式、已知问题和不可测试项
- 固定句式：”加载 auto-test-demo skill 并按其指引完成自动化测试“

要求 subagent 只返回：

```markdown
## Result

- status: completed / failed / blocked
- summary_file: doc-test-reports/{run-name}/auto-test/test-summary.md
- detail_files:
  - doc-test-reports/{run-name}/auto-test/test-report.md
  - doc-test-reports/{run-name}/auto-test/test-cases.json
  - doc-test-reports/{run-name}/auto-test/test-cases.sh
  - doc-test-reports/{run-name}/auto-test/test-results.jsonl
- artifact_dirs:
  - doc-test-reports/{run-name}/auto-test/logs/
  - doc-test-reports/{run-name}/auto-test/screenshots/
- document_link: auto-test/test-summary.md
- summary: 测试是否通过，通过/失败/跳过用例数，关键失败原因
- next_action: continue / stop / needs_user_input
```

完成后验证 `auto-test-demo` 要求的关键产物存在，并更新 `run-index.md`。`auto-test-demo` subagent 只负责测试用例设计、测试脚本生成、测试执行、截图、日志采集和失败诊断；不要让它在内部修复 demo 代码或为了通过测试改低预期。

如果自动化测试失败，主会话读取 `test-summary.md`、`test-report.md`、`test-results.jsonl` 和必要日志，按失败分析决定是否修复后重测。不要在总控里凭截图或症状重新判断，必须依据 `auto-test-demo` 已采集的诊断信息。

修复和重测流程：

1. 判断失败类型：
   - **测试环境或测试脚本问题**：例如设备未启动、浏览器会话残留、端口冲突、测试目标连接失败。由主会话修复环境、调整 `test-cases.json` 的 `runtime.*Commands` 或重新生成测试脚本。
   - **demo 实现问题**：例如按文档构建出的 demo 代码有实现遗漏、初始化错误、UI 无法触发核心流程。由主会话直接修复 `doc-test-reports/{run-name}/examples/{demo-name}/`；修复依据必须来自目标文档、构建验证报告和自动化测试失败分析。
   - **文档/SDK/测试产物问题**：如果失败原因是文档缺失、SDK 行为异常、测试产物不可用或用户资料不足，可以搜索整个工作区找到必要文档说明后修复，但是要记录为最终主报告的问题证据。
2. 如果执行了环境、脚本或 demo 修复，主会话先执行必要的编译/运行验证。
3. 把本轮失败原因、修复内容、验证结果写入：

```text
doc-test-reports/{run-name}/auto-test/repair-attempts.md
```

4. 启动新的 `auto-test-demo` subagent 重测。传入本次任务简介、用户特殊要求、项目目录、报告目录、上一轮测试报告路径、`repair-attempts.md`，并再次明确要求加载并使用 `auto-test-demo` skill，只重新测试和诊断，不执行修复。

最多进行 3 轮“主会话修复 + 新 subagent 重测”。每轮都要更新 `repair-attempts.md` 和 `run-index.md` 说明列。

### Step 5: 整理报告发布输入

将 `report-publish` 置为 `running`。确认以下本地产物存在，并整理成给报告发布 subagent 的输入清单：

- `doc-test-reports/{run-name}/doc-eval/doc-eval-summary.md`
- `doc-test-reports/{run-name}/doc-eval/role-*.md`
- `doc-test-reports/{run-name}/build-verification/build-summary.md`
- `doc-test-reports/{run-name}/build-verification/build-issues.md`
- `doc-test-reports/{run-name}/auto-test/test-summary.md`（如存在）
- `doc-test-reports/{run-name}/auto-test/test-report.md`（如存在）
- `doc-test-reports/{run-name}/auto-test/test-results.jsonl`（如存在）
- `doc-test-reports/{run-name}/auto-test/screenshots/`（如存在）
- `doc-test-reports/{run-name}/auto-test/logs/`（如存在）
- `doc-test-reports/{run-name}/examples/{demo-name}/`
- `doc-test-reports/{run-name}/run-index.md`

不要在主会话里生成最终飞书报告内容。最终飞书报告、校正后 doc-eval 报告和附件上传交给 `report-doc-test-in-feishu` skill。

### Step 6: 按需写入飞书

如果用户要求不写飞书，跳过本步骤，最终回复给出本地目录和关键报告路径。

如果需要写入飞书，启动独立 subagent，prompt 要求加载并使用 `report-doc-test-in-feishu` skill，按该 skill 指引完成报告创建、内容写入、附件上传和链接回写；不要在主会话 prompt 中写一套飞书报告生成流程来替代它。传入：

- 本次任务简介和用户特殊要求
- 本地 run 目录：`doc-test-reports/{run-name}/`
- 固定句式：”加载 report-doc-test-in-feishu skill 并按其指引发布飞书报告“

只有在 `report-doc-test-in-feishu` 无法从 run 目录推断时，才补充传入产品、平台、范围、日期、`demo-name`、目标文档列表、已有飞书节点或实际 `midscene_run` 路径。

`report-doc-test-in-feishu` 必须完成两类飞书报告，并把最终结论集中到 `【文档评测报告】汇总报告`：

1. **构建与自动化测试报告**：根据 build-verification 和 auto-test 生成并写入飞书，同时上传自动化测试报告压缩包、截图、源码压缩包。
2. **校正后的 doc-eval 报告**：根据 build-verification 和 auto-test 校正 doc-eval 本地 Markdown，然后创建并写入各角色报告和 summary 飞书文档。`【文档评测报告】汇总报告` 是最终主报告，必须合并角色评分、问题摘要、问题详情、构建/测试新增或校正问题。

要求 report subagent 只返回：

```markdown
## Result

- status: completed / failed / blocked
- feishu_folder: {folder_url}
- build_test_report: {url}
- doc_eval_summary: {url}
- doc_eval_roles:
  - {role-id}: {url}
- local_links_file: doc-test-reports/{run-name}/feishu-report-links.md
- summary: {一句话说明发布结果}
- next_action: continue / stop / needs_user_input
```

完成后验证 `feishu-report-links.md` 和 `run-index.md` 已更新。飞书写入失败时不要丢弃本地产物；在 `run-index.md` 的 `report-publish` 说明列记录失败原因和已完成的本地报告路径。

### Step 7: 回复用户

最终回复只给高信号结论：

- 本地报告目录
- 如已写飞书，飞书文件夹和最终报告链接
- 文档评测评分和校正结论
- 构建是否成功
- 自动化测试是否通过
- 阻塞问题数量和最高优先级问题

不要粘贴完整报告内容。
