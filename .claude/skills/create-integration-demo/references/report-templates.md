# 构建验证输出模板

本模板用于输出构建验证摘要、步骤记录和问题详情。

## 输出位置

构建验证报告写入：

```text
doc-test-reports/{run-name}/build-verification/
  build-summary.md
  build-steps.md
  build-issues.md
  logs/
```

示例代码写入：

```text
doc-test-reports/{run-name}/examples/{demo-name}/
```

`run-name` 固定格式：

```text
{product}-{platform}-{scope}-{date}
```

## GitHub 定位要求

凡是文档导致的问题，定位必须是有效 GitHub 链接，不能只写章节名、本地路径或“前提条件章节”。

请参考 file-to-github-link skill 指引获取GitHub链接。

非文档问题可以定位到日志、代码路径或命令输出文件。

## 关联文档问题链接要求

构建验证中如果关联到 `doc-eval` 阶段的问题，不能只写 `DOC-001`。

本地 Markdown 产物中，应写成相对链接：

```markdown
[DOC-001](../doc-eval/role-client-dev.md#doc-001-appid-获取路径缺失)
```

如果关联问题只出现在文档评测汇总中，可以链接到：

```markdown
[DOC-001](../doc-eval/doc-eval-summary.md#doc-001-appid-获取路径缺失)
```

写入飞书文档后，应改成飞书报告链接 + 问题 ID + 问题详情章节标题。若后续可以通过飞书 API 获取标题 block 链接，再升级为章节级飞书链接。

## build-summary.md 模板

```markdown
# 构建验证摘要

## 基本信息

| 字段 | 值 |
|------|----|
| 产品 | {product} |
| 平台 | {platform} |
| 范围 | {scope} |
| 目标文档 | {doc_path_1}<br>{doc_path_2}<br>{...} |
| 示例项目目录 | doc-test-reports/{run-name}/examples/{demo-name} |
| 报告目录 | doc-test-reports/{run-name}/ |
| 构建日期 | {date} |

## 阶段结论

| 字段 | 值 |
|------|----|
| 状态 | completed / failed / blocked |
| 是否成功生成项目 | 是 / 否 |
| 是否安装依赖成功 | 是 / 否 |
| 是否编译通过 | 是 / 否 |
| 是否能启动运行 | 是 / 否 / 未执行 |
| 阻塞问题数 | N |
| 体验问题数 | N |
| 优化建议数 | N |
| 一句话结论 | {一句话概括构建验证结果} |

## 关键发现

- {关键发现 1}
- {关键发现 2}

## 关键步骤结果

| 步骤 ID | 步骤 | 状态 | 文档定位 | 操作 | 结果 | 详情 |
|---------|------|------|----------|------|------|------|
| STEP-001 | 安装 SDK | completed | [docs/xxx.mdx:88](https://github.com/...) | npm install ... | 成功 | build-steps.md#step-001 |
| STEP-002 | 编译项目 | failed | - | npm run build | 失败 | logs/build.log |

## 问题摘要

| 问题 ID | 构建步骤 | 定位 | 类别 | 严重度 | 问题 | 关联文档问题 |
|---------|----------|------|------|--------|------|------|
| BUILD-001 | 编译项目 | logs/build.log | 🔧 代码实现问题 | 🔴 阻塞 | {一句话问题} | [DOC-002](../doc-eval/role-client-dev.md#doc-002-token-说明不足) |

## 与前置阶段的关系

| 当前问题 ID | 前置问题 ID | 关系 | 说明 |
|-------------|-------------|------|------|
| BUILD-001 | [DOC-002](../doc-eval/role-client-dev.md#doc-002-token-说明不足) | 复现 / 延续 / 部分复现 / 未复现 / 新增 / 重复 | {说明} |

## 自动化测试输入

| 项目 | 内容 |
|------|------|
| 推荐是否继续自动化测试 | 是 / 否 |
| 原因 | {说明} |
| 继续测试前需要处理 | {问题 ID 或无} |
| 测试入口 | {启动命令、URL、包名或应用路径} |

## 产物索引

| 类型 | 路径 |
|------|------|
| 构建摘要 | build-summary.md |
| 构建步骤详情 | build-steps.md |
| 构建问题详情 | build-issues.md |
| 安装日志 | logs/install.log |
| 编译日志 | logs/build.log |
| 示例项目 | ../examples/{demo-name} |
```

## build-steps.md 模板

```markdown
# 构建步骤详情

## STEP-001: {步骤名称}

- 状态：completed / failed / blocked
- 文档定位：[docs/xxx.mdx:123](https://github.com/...)
- 执行操作：{命令或代码操作}
- 结果：{执行结果}
- 日志：logs/{xxx}.log

**文档原文**

```markdown
{文档原文摘录}
```

**执行记录**

```bash
{关键命令}
```

**说明**

{必要说明}
```

## build-issues.md 模板

```markdown
# 构建验证问题详情

## BUILD-001: {问题标题}

- 构建步骤：{步骤名}
- 定位：[docs/xxx.mdx:123](https://github.com/...) 或 logs/build.log
- 类别：📄 文档问题 / 🔧 代码实现问题 / 🏗️ 环境问题 / 🔗 链接问题 / 📖 概念缺失
- 严重度：🔴 阻塞 / 🟡 体验差 / 🟢 优化建议
- 关联文档问题：[DOC-002](../doc-eval/role-client-dev.md#doc-002-token-说明不足) / 无

**证据**

```markdown
{如果是文档问题，摘录文档原文。}
```

```log
{如果是构建或运行问题，摘录关键日志。}
```

**实际操作或观察**

{执行了什么，发生了什么。}

**为什么是问题**

{从零经验开发者严格按文档执行的角度说明。}

**建议**

{具体修复建议。}
```

## subagent 返回要求

完成后只返回：

```markdown
## Result

- status: completed / failed / blocked
- summary_file: doc-test-reports/{run-name}/build-verification/build-summary.md
- detail_files:
  - doc-test-reports/{run-name}/build-verification/build-steps.md
  - doc-test-reports/{run-name}/build-verification/build-issues.md
- document_link: doc-test-reports/{run-name}/build-verification/build-summary.md
- summary: 发现 N 个问题，其中 M 个阻塞
- next_action: continue / stop / needs_user_input
```
