# 自动化测试输出模板

本模板用于输出测试摘要、测试用例、测试脚本和完整测试报告。

## 输出位置

测试报告写入：

```text
doc-test-reports/{run-name}/auto-test/
  test-cases.json
  test-summary.md
  test-cases.sh
  test-report.md
  test-results.jsonl
  logs/
  screenshots/
```

`run-name` 固定格式：

```text
{product}-{platform}-{scope}-{date}
```

## test-cases.sh 执行目录要求

`test-cases.sh` 可以保存在报告目录，但执行时必须切到正确项目目录。

脚本开头必须包含类似逻辑：

```bash
#!/bin/bash
set +e
set -o pipefail

REPORT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$REPORT_DIR/../../.." && pwd)"
PROJECT_DIR="$REPO_ROOT/doc-test-reports/{run-name}/examples/{demo-name}"

cd "$PROJECT_DIR" || exit 1
```

不要假设用户会从项目目录手动执行脚本。

## 关联前置问题链接要求

自动化测试中如果关联到前置构建验证或文档评测问题，不能只写 `BUILD-001` 或 `DOC-001`。

本地 Markdown 产物中，应写成相对链接：

```markdown
[BUILD-001](../build-verification/build-issues.md#build-001-token-生成逻辑缺失)
[DOC-001](../doc-eval/role-client-dev.md#doc-001-appid-获取路径缺失)
```

如果关联问题只出现在前置阶段摘要中，可以链接到对应摘要文件：

```markdown
[BUILD-001](../build-verification/build-summary.md#build-001-token-生成逻辑缺失)
[DOC-001](../doc-eval/doc-eval-summary.md#doc-001-appid-获取路径缺失)
```

写入飞书文档后，应改成飞书报告链接 + 问题 ID + 问题详情章节标题。若后续可以通过飞书 API 获取标题 block 链接，再升级为章节级飞书链接。

## test-summary.md 模板

```markdown
# 自动化测试摘要

## 基本信息

| 字段 | 值 |
|------|----|
| 产品 | {product} |
| 平台 | {platform} |
| 范围 | {scope} |
| 目标文档 | {doc_path_1}<br>{doc_path_2}<br>{...，可选} |
| 示例项目目录 | doc-test-reports/{run-name}/examples/{demo-name} |
| 报告目录 | doc-test-reports/{run-name}/ |
| 测试日期 | {date} |

## 阶段结论

| 字段 | 值 |
|------|----|
| 状态 | completed / failed / blocked |
| 总用例数 | N |
| 通过 | N |
| 失败 | N |
| 跳过 | N |
| 通过率 | X% |
| 阻塞问题数 | N |
| 一句话结论 | {一句话概括测试结果} |

## 关键发现

- {关键发现 1}
- {关键发现 2}

## 用例结果

| 用例 ID | 用例名称 | 依赖 | 状态 | 截图 | 日志 | 关联问题 |
|---------|----------|------|------|------|------|----------|
| TC-001 | 登录 - Alice | - | passed | screenshots/TC-001.png | - | - |
| TC-002 | 加入房间 | TC-001 | failed / skipped | screenshots/TC-002.png | logs/TC-002-console.log | TEST-001 |

## 问题摘要

| 问题 ID | 用例 ID | 截图/日志 | 类别 | 严重度 | 问题 | 关联前置问题 |
|---------|---------|-----------|------|--------|------|--------------|
| TEST-001 | TC-002 | screenshots/TC-002.png / logs/TC-002-console.log | 📄 文档问题 | 🔴 阻塞 | {一句话问题} | [BUILD-001](../build-verification/build-issues.md#build-001-token-生成逻辑缺失) |

## 与前置阶段的关系

| 当前问题 ID | 前置问题 ID | 关系 | 说明 |
|-------------|-------------|------|------|
| TEST-001 | [BUILD-001](../build-verification/build-issues.md#build-001-token-生成逻辑缺失) | 延续 / 复现 / 部分复现 / 未复现 / 新增 / 重复 | {说明} |

## 修复与最终汇总提示

| 项目 | 内容 |
|------|------|
| 是否需要修复后重测 | 是 / 否 |
| 优先处理问题 | TEST-001 |
| 建议操作 | {修复建议或下一步} |

## 产物索引

| 类型 | 路径 |
|------|------|
| 测试摘要 | test-summary.md |
| 测试用例数据 | test-cases.json |
| 测试脚本 | test-cases.sh |
| 测试结果数据 | test-results.jsonl |
| 完整测试报告 | test-report.md |
| 截图目录 | screenshots/ |
| 日志目录 | logs/ |
```

## test-report.md 模板

```markdown
# 自动化测试报告

## 测试环境

| 字段 | 值 |
|------|----|
| 操作系统 | {OS} |
| 平台 | {Web/Android/iOS/Desktop/HarmonyOS} |
| 浏览器/运行时 | {Chrome/Android/iOS 等} |
| SDK 版本 | {SDK version} |
| 必要包的版本 | {如Node.js version} |
| 示例项目目录 | doc-test-reports/{run-name}/examples/{demo-name} |

## 测试概览

| 指标 | 值 |
|------|----|
| 总用例数 | N |
| 通过 | N |
| 失败 | N |
| 跳过 | N |
| 通过率 | X% |

## 用例结果

| 用例 ID | 用例名称 | 依赖 | 前提条件 | 状态 | 截图 | 问题 ID |
|---------|----------|------|----------|------|------|---------|
| TC-001 | {名称} | - | {前提条件} | passed | screenshots/TC-001.png | - |
| TC-002 | {名称} | TC-001 | {前提条件} | failed / skipped | screenshots/TC-002.png | TEST-001 |

## 失败用例分析

### TEST-001 / TC-002: {用例名称}

- 类别：📄 文档问题 / 🔧 代码实现问题 / 🏗️ 环境问题 / 🔗 链接问题 / 📖 概念缺失
- 严重度：🔴 阻塞 / 🟡 体验差 / 🟢 优化建议
- 截图：screenshots/TC-002.png
- 日志：logs/TC-002-console.log
- 关联前置问题：[BUILD-001](../build-verification/build-issues.md#build-001-token-生成逻辑缺失) / [DOC-001](../doc-eval/role-client-dev.md#doc-001-appid-获取路径缺失) / 无

**失败表现**

{从截图或 act 输出描述表面现象。}

**系统日志**

```log
{主动采集到的 console / logcat / Xcode log 等关键片段。}
```

**综合原因**

{必须结合失败表现和系统日志分析。不能只凭截图表面现象推断。}

**建议修复方向**

{具体建议。}

## 通过用例备注

{如有通过但存在异常日志的用例，在此补充。没有则写“无”。}
```

## subagent 返回要求

完成后只返回：

```markdown
## Result

- status: completed / failed / blocked
- summary_file: doc-test-reports/{run-name}/auto-test/test-summary.md
- detail_files:
  - doc-test-reports/{run-name}/auto-test/test-cases.json
  - doc-test-reports/{run-name}/auto-test/test-report.md
  - doc-test-reports/{run-name}/auto-test/test-cases.sh
  - doc-test-reports/{run-name}/auto-test/test-results.jsonl
- document_link: doc-test-reports/{run-name}/auto-test/test-summary.md
- summary: 总用例 N 个，通过 M 个，失败 K 个
- next_action: continue / stop / needs_user_input
```
