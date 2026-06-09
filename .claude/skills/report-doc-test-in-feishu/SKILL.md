---
name: report-doc-test-in-feishu
description: >
  Use this skill when the user needs to publish a ZEGO documentation access-test run to Feishu:
  create fixed report documents under the access-test Feishu node, correct doc-eval reports using
  build and auto-test results, write build/test and final integration reports, upload source/test
  artifacts and screenshots, and return Feishu links. Triggers on: "写入飞书接入测试报告",
  "发布接入测试报告", "report-doc-test-in-feishu", "飞书报告", "生成飞书报告", or when
  make-integration-test reaches its Feishu publishing stage.
version: 1.0.0
---

# 接入测试飞书报告发布

根据一次接入测试 run 的本地产物，创建并写入固定飞书报告。主输入是任务简介和本地 run 目录；阶段报告、示例项目、截图、日志和自动化运行报告优先从 run 目录扫描发现。

## 输入

必须传入：

- 本次任务简介和用户特殊要求
- 本地 run 目录：`doc-test-reports/{run-name}/`

可选传入：

- 产品、平台、范围、日期、`run-name`、`demo-name`：无法从目录名、`run-index.md` 或阶段报告推断时再传。
- 目标文档列表：无法从 `run-index.md` 或 doc-eval 报告推断时再传。
- 已创建的飞书节点、文档 ID 或 `feishu-report-manifest.json`：用于续写或重试。
- 自动化工具运行报告目录：例如某次测试实际生成的 `midscene_run`。不传时在 run 目录下扫描。

## 产物发现

先扫描本地 run 目录，建立本次发布使用的产物清单：

| 产物 | 默认发现位置 | 缺失处理 |
|------|--------------|----------|
| run index | `run-index.md` | 缺失时继续，但不能回写阶段链接 |
| doc-eval 汇总 | `doc-eval/doc-eval-summary.md` | 必须存在 |
| doc-eval 角色报告 | `doc-eval/role-*.md` | 至少一个角色报告 |
| 构建汇总 | `build-verification/build-summary.md` | 必须存在 |
| 构建问题 | `build-verification/build-issues.md` | 缺失时按无独立问题明细处理，并在报告说明 |
| 自动化测试汇总 | `auto-test/test-summary.md` | 自动化阶段跳过时可缺失 |
| 自动化测试明细 | `auto-test/test-report.md`、`auto-test/test-results.jsonl` | 自动化阶段跳过时可缺失 |
| 截图目录 | `auto-test/screenshots/` | 缺失时跳过截图上传 |
| 日志目录 | `auto-test/logs/` | 缺失时仅不引用日志 |
| 示例项目目录 | `examples/*/` | 多个目录时用传入的 `demo-name` 匹配；仍无法确定则先询问 |
| 自动化运行报告目录 | 优先使用传入路径；否则搜索 `auto-test/midscene_run`、`examples/{demo-name}/midscene_run`、`**/midscene_run` | 缺失时跳过该附件 |

从 `run-name` 目录名按 `{product}-{platform}-{scope}-{date}` 推断产品、平台、范围、日期；推断失败时用传入值或从 `run-index.md`、阶段报告标题补齐。

## 输出

本 skill 至少输出：

```text
doc-test-reports/{run-name}/feishu-report-manifest.json
doc-test-reports/{run-name}/feishu-report-links.md
doc-test-reports/{run-name}/build-test-report.md
doc-test-reports/{run-name}/integration-summary.md
doc-test-reports/{run-name}/doc-eval-corrected/
```

飞书中固定创建：

| 报告类型 | 飞书文档标题 | 数据来源 |
|----------|--------------|----------|
| build-test-report | `构建与自动化测试报告` | build-verification + auto-test |
| doc-eval-summary | `【文档评测报告】汇总报告` | doc-eval + build-verification + auto-test |
| doc-eval-role | `【文档评测报告】{role-name}` | 对应 role report + build-verification + auto-test |
| integration-summary | `接入测试综合报告` | 校正后 doc-eval + build-test-report |

角色报告枚举按本地 `doc-eval/role-*.md` 文件决定。常见角色 ID：`role-cto`、`role-support`、`role-client-dev`、`role-server-dev`、`role-fullstack-dev`。

飞书子文档标题不重复任务名；任务名只保留在总节点标题里。

## 写入飞书文档

Step 2、Step 3、Step 4 生成本地 Markdown 后，先运行发布前定位预检查：

```bash
node .claude/skills/report-doc-test-in-feishu/scripts/validate-report-locations.js \
  --run-dir "doc-test-reports/{run-name}"
```

如果脚本发现空定位，或定位字段中出现 `.mdx` 但不是 GitHub 链接，先回到本地 Markdown 修复定位，再继续发布。类似 `同客户端开发角色报告中的 DOC-002` 这种跨报告引用不要求转换为 GitHub 链接。

定位预检查通过后，运行发布前预处理：

```bash
node .claude/skills/report-doc-test-in-feishu/scripts/prepare-feishu-report-content.js \
  --run-dir "doc-test-reports/{run-name}"
```

该脚本会：

- 将本地报告 H1 对齐为 `feishu-report-manifest.json` 中的飞书文档标题。
- 将文档评测汇总报告 `角色评分` 表格中的本地角色报告路径替换为 manifest 中的飞书链接。
- 在 `角色评分` 表格后追加：`**请阅读各角色详细报告文档并评论问题解决方案！**`
- 将 `build-verification/build-issues.md` 合并到 `build-test-report.md` 的 `关键问题` 后，作为 `问题详情` 章节。

然后写入飞书：

1. 确认本地 Markdown 第一行是 `# {报告标题}`。
2. 从 `doc-test-reports/{run-name}/feishu-report-manifest.json` 读取目标文档 ID。
3. 使用 `scripts/write-feishu-markdown.sh` 覆盖写入目标飞书文档。
4. 记录目标飞书 URL，供 `feishu-report-links.md` 和 `run-index.md` 使用。

读取固定报告 docId：

```bash
node -e '
const fs = require("fs");
const manifest = JSON.parse(fs.readFileSync(process.argv[1], "utf8"));
const reportType = process.argv[2];
const doc = manifest.documents && manifest.documents[reportType];
if (!doc || !doc.docId) process.exit(1);
console.log(doc.docId);
' "doc-test-reports/{run-name}/feishu-report-manifest.json" "{reportType}"
```

读取角色报告 docId：

```bash
node -e '
const fs = require("fs");
const manifest = JSON.parse(fs.readFileSync(process.argv[1], "utf8"));
const roleId = process.argv[2];
const doc = manifest.documents && manifest.documents["doc-eval-role"] && manifest.documents["doc-eval-role"][roleId];
if (!doc || !doc.docId) process.exit(1);
console.log(doc.docId);
' "doc-test-reports/{run-name}/feishu-report-manifest.json" "{role-id}"
```

写入命令：

```bash
bash .claude/skills/report-doc-test-in-feishu/scripts/write-feishu-markdown.sh \
  --doc-id "{doc_id}" \
  --file "{local_markdown_file}"
```

`--file` 必须是本地 Markdown 文件。不要把文件路径直接传给 `lark-cli docs +update --content`；脚本会通过 stdin 把文件内容写入飞书。

## 流程

### Step 1: 创建飞书文档骨架

先完成「产物发现」，确认 `run-dir`、`demo-dir`、`role-files`、`midscene_run` 等实际路径。之后读取 `references/feishu-report-skeletons.md`，使用其中的固定节点和文档类型说明。

优先使用脚本创建飞书节点和文档骨架：

```bash
bash scripts/create-feishu-report-skeletons.sh \
  --run-dir "doc-test-reports/{run-name}" \
  --product "{product}" \
  --platform "{platform}" \
  --scope "{scope}" \
  --date "{date}" \
  --role-files "{role_files_glob}"
```

脚本会创建：

```text
doc-test-reports/{run-name}/feishu-report-manifest.json
```

如果脚本因为 lark-cli 权限、网络或参数问题失败，按 `references/feishu-report-skeletons.md` 手动创建同样的文档骨架，并写出同样结构的 manifest。

### Step 2: 生成构建与自动化测试报告

读取 `references/report-content-templates.md` 的「构建与自动化测试报告」模板。

根据 `build-verification/` 和 `auto-test/` 产物生成：

```text
doc-test-reports/{run-name}/build-test-report.md
```

写入前必须先运行 `validate-report-locations.js`，发现定位问题就修复本地 Markdown；通过后再运行 `prepare-feishu-report-content.js`，确保 `build-verification/build-issues.md` 已合并为 `## 问题详情`。

写入飞书：

1. 从 manifest 读取 `documents["build-test-report"].docId`。
2. 调用 `scripts/write-feishu-markdown.sh --doc-id "{doc_id}" --file "doc-test-reports/{run-name}/build-test-report.md"`。
3. 从 manifest 读取 `documents["build-test-report"].url`，后续写入 `feishu-report-links.md` 和 `run-index.md`。

附件上传要求：

- 源码压缩包：清理 `doc-test-reports/{run-name}/examples/{demo-name}/` 后打包并上传。
- 自动化运行报告压缩包：按发现到的运行报告目录打包，例如 `midscene_run`；不要默认压缩整个 `auto-test/` 目录。
- 截图：将 `auto-test/screenshots/` 下的关键截图插入构建与自动化测试报告的截图章节。

使用 `scripts/upload-feishu-report-assets.sh` 完成打包和上传，参数说明见 `references/feishu-upload.md`。

### Step 3: 校正文档评测报告

读取「产物发现」中确认的原始报告，默认路径为：

```text
doc-test-reports/{run-name}/doc-eval/doc-eval-summary.md
doc-test-reports/{run-name}/doc-eval/role-*.md
doc-test-reports/{run-name}/build-verification/build-summary.md
doc-test-reports/{run-name}/build-verification/build-issues.md
doc-test-reports/{run-name}/auto-test/test-summary.md
doc-test-reports/{run-name}/auto-test/test-report.md
```

如果自动化测试阶段被跳过，基于 doc-eval 和 build-verification 完成校正，并在校正报告中说明自动化证据缺失。

生成校正后的本地 Markdown：

```text
doc-test-reports/{run-name}/doc-eval-corrected/doc-eval-summary.md
doc-test-reports/{run-name}/doc-eval-corrected/role-*.md
```

写入前必须先运行 `validate-report-locations.js`，发现定位问题就修复本地 Markdown；通过后再运行 `prepare-feishu-report-content.js`，确保 summary 里的角色报告链接已经替换为飞书链接，并已加入加粗提醒语。

校正规则：

- 用构建验证和自动化测试结果确认、降级、升级或撤销 doc-eval 发现。
- 校正后的角色报告必须以原 `doc-eval/role-*.md` 为底稿重写正文，不要只在末尾追加校正章节。
- 原始角色报告中已有的 `定位` GitHub 链接必须原样保留。校正时可以新增 `构建/测试证据`、校正后严重程度和说明，但不能把原定位改写成文件名、章节名、所有文档、同某角色报告等弱定位。
- 同一角色同一问题 ID 在 `doc-eval-corrected/role-*.md` 中必须保留 `doc-eval/role-*.md` 里已有的 GitHub 定位 URL；新增问题 `DOC-N-*` 才需要补充新的 GitHub 定位。
- 角色报告的 `问题摘要` 表格要增加 `构建测试校正后严重程度` 列。
- 角色报告的问题详情中要保留原严重度，并增加 `构建测试校正后严重程度`、`构建/测试证据` 和 `构建/测试校正结果`。
- `为什么是问题` 和 `建议` 要结合构建/测试结果改写：已复现的问题说明真实阻塞点；未复现但仍影响体验的问题降级说明；原判断不成立的问题标记撤销并解释原因。
- build/test 复现的问题要链接回原 doc-eval 问题。
- build/test 新增且属于文档质量的问题，要加入校正后 summary。
- 不把 demo 实现问题、设备问题、SDK 测试产物问题错误归咎为文档问题。

写入飞书：

1. 汇总报告：从 manifest 读取 `documents["doc-eval-summary"].docId`，将 `doc-test-reports/{run-name}/doc-eval-corrected/doc-eval-summary.md` 写入该文档。
2. 角色报告：对每个 `doc-test-reports/{run-name}/doc-eval-corrected/role-*.md`，用文件名去掉 `.md` 得到 `role-id`，从 manifest 读取 `documents["doc-eval-role"][role-id].docId`，将该角色 Markdown 写入对应飞书文档。
3. 每个文档写入后，从 manifest 读取对应 `url`，用于生成 `feishu-report-links.md`。

### Step 4: 生成接入测试综合报告

读取校正后的 doc-eval 报告和 `build-test-report.md`，生成：

```text
doc-test-reports/{run-name}/integration-summary.md
```

写入前必须先运行 `validate-report-locations.js`，发现定位问题就修复本地 Markdown；通过后再运行 `prepare-feishu-report-content.js`，确保本地 H1 与 manifest 中的飞书文档标题一致。

综合报告只做整体说明：

- 各阶段结果
- 真实接入结论
- 最终优先级问题
- 建议动作和责任归属
- 飞书报告和附件索引

不要在综合报告里替代各阶段报告的完整细节。

写入飞书：

1. 从 manifest 读取 `documents["integration-summary"].docId`。
2. 调用 `scripts/write-feishu-markdown.sh --doc-id "{doc_id}" --file "doc-test-reports/{run-name}/integration-summary.md"`。
3. 从 manifest 读取 `documents["integration-summary"].url`，后续写入 `feishu-report-links.md` 和 `run-index.md`。

### Step 5: 回写索引和返回结果

写出：

```text
doc-test-reports/{run-name}/feishu-report-links.md
```

更新 `run-index.md` 的 `文档链接` 列：

- `doc-eval`：校正后 summary 飞书链接
- `build-verification`：构建与自动化测试报告飞书链接
- `auto-test`：构建与自动化测试报告飞书链接
- `integration-summary`：接入测试综合报告飞书链接

最终只返回：

```markdown
## Result

- status: completed / failed / blocked
- feishu_folder: {folder_url}
- build_test_report: {url}
- doc_eval_summary: {url}
- doc_eval_roles:
  - {role-id}: {url}
- integration_summary: {url}
- local_links_file: doc-test-reports/{run-name}/feishu-report-links.md
- summary: {一句话说明发布结果}
- next_action: continue / stop / needs_user_input
```

## 飞书操作

涉及飞书文档、云盘、知识库时，按 `lark-wiki`、`lark-doc`、`lark-drive` skill 指引操作。`lark-cli docs +update --content` 接收字符串、`-` 或受限的相对 `@file`；写入本地 Markdown 报告统一使用 `scripts/write-feishu-markdown.sh`。
