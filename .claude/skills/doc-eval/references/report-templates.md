# 文档评测汇总报告输出格式

本模板用于 `doc-eval` 的阶段摘要和文档评测汇总报告。

## 输出位置

`doc-eval` 阶段至少输出：

```text
doc-test-reports/{run-name}/doc-eval/doc-eval-summary.md
doc-test-reports/{run-name}/doc-eval/role-*.md
```

`run-name` 固定格式：

```text
{product}-{platform}-{scope}-{date}
```

## 飞书写入策略

在本地文件创建后，默认还要写入飞书。

如果用户明确要求“不写飞书”“只输出本地 Markdown”“不要上传”，则只生成本地 Markdown，不写飞书。


## doc-eval-summary.md 模板

```markdown
# 文档评测摘要

## 基本信息

| 字段 | 值 |
|------|----|
| 产品 | {product} |
| 平台 | {platform} |
| 范围 | {scope} |
| 文档类型 | {doc_type} |
| 目标文档 | {doc_path_1}<br>{doc_path_2}<br>{...} |
| 评测日期 | {date} |

## 阶段结论

| 字段 | 值 |
|------|----|
| 状态 | completed / failed / blocked |
| 加权平均分 | X/5 |
| 参与角色 | {角色列表} |
| 阻塞问题数 | N |
| 体验问题数 | N |
| 优化建议数 | N |
| 一句话结论 | {一句话概括文档质量} |

## 角色评分

| 角色 | 匹配度 | 加权平均分 | 维度评分 | 报告 |
|------|--------|------------|----------|------|
| 客户端开发 | ★★★★★ | X/5 | - 完整性：X/5<br>- 准确性：X/5<br>- 可执行性：X/5<br>- 排障支持：X/5 | role-client-dev.md |

## 问题摘要

| 问题 ID | 角色 | 定位 | 类别 | 严重度 | 问题 | 建议 |
|---------|------|------|------|--------|------|------|
| DOC-001 | 客户端开发 | [docs/xxx.mdx:123](https://github.com/ZEGOCLOUD/docs_all/blob/main/docs/xxx.mdx?plain=1#L123) | 📄 文档问题 | 🔴 阻塞 | {一句话问题} | {一句话建议} |

## 问题详情

问题详情必须与 `问题摘要` 顺序一一对应。同一问题被多个角色发现时，合并为一个问题详情，并在 `角色` 字段写多个角色。

### DOC-001 {问题标题}

- 严重度：🔴 阻塞 / 🟡 体验差 / 🟢 优化建议
- 类别：📄 文档问题 / 🔗 链接问题 / 📖 概念缺失
- 角色：客户端开发、全栈开发
- 定位：[docs/xxx.mdx:123](https://github.com/ZEGOCLOUD/docs_all/blob/main/docs/xxx.mdx?plain=1#L123)

**为什么是问题**

{照搬或合并角色报告中的问题详情描述。}

**建议**

{照搬或合并角色报告中的建议。}
```
