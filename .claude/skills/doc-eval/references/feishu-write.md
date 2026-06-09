# 飞书写入说明

## 创建任务文件夹

在飞书知识库的「接入测试」节点下创建本次评测的文件夹。

父节点信息：

- space_id: `7187666870011232257`
- parent_node_token: `Bvy6wsTvjiLh7bkzOxVcwvyunTH`

```bash
lark-cli wiki nodes create --params '{"space_id":"7187666870011232257"}' --data '{"parent_node_token":"Bvy6wsTvjiLh7bkzOxVcwvyunTH","node_type":"origin","obj_type":"docx","title":"【YY-MM-DD 产品名-平台-范围 文档评测】"}' --as user
```

注意：

- `space_id` 是 path 参数，必须用 `--params` 传。
- body 参数用 `--data` 传。
- 两者分开。

## 创建并写入文档

写入飞书文档时分两步。

### 创建空文档

```bash
lark-cli docs +create --api-version v2 --parent-token {folder_node_token} --doc-format markdown --content "$(cat <<'EOF'
# 标题
EOF
)"
```

### overwrite 写入完整内容

`--content` 接收字符串，不是文件路径。

```bash
lark-cli docs +update --api-version v2 --doc {document_id} --command overwrite --doc-format markdown --content "$(cat <<'EOF'
# 标题
... 完整报告 markdown 内容 ...
EOF
)"
```

## 注意事项

- `--content` 直接接收字符串，不能用 `@-`（stdin）或 `@file.md`（文件路径）。
- 内容较长时用 `$(cat <<'EOF' ... EOF)` heredoc 包裹。
- `docs +create` 的 `--content` 参数必填，不能为空。
- 长文档可先 `+create` 建骨架，再用 `+update --command append` 分段追加。
- 文档标题从内容中的 `#`（h1）提取，确保 overwrite 内容第一行是 `# 标题`。

## 写入范围

建议写入：

- `doc-eval/doc-eval-summary.md`
- `doc-eval/role-*.md`

写入完成后，在 subagent 返回结果里附上：

- 飞书任务文件夹链接
- 各角色评测报告飞书链接
- 汇总报告飞书链接
