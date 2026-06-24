# 飞书报告骨架

## 固定知识库节点

默认在飞书知识库「接入测试」节点下创建本次 run 的文档集合。

- `space_id`: `7187666870011232257`
- `parent_node_token`: `Bvy6wsTvjiLh7bkzOxVcwvyunTH`

任务节点标题：

```text
【{date} {product}-{platform}-{scope} 接入测试】
```

## 固定报告类型

| reportType | 是否固定 | 标题 |
|------------|----------|------|
| build-test-report | 是 | `构建与自动化测试报告` |
| doc-eval-summary | 是 | `【文档评测报告】汇总报告` |
| doc-eval-role | 按角色枚举 | `【文档评测报告】{role-name}` |

文档评测组统一使用 `【文档评测报告】` 前缀，包括汇总报告和各角色报告。构建测试报告不加阶段前缀。子文档标题不重复产品、平台、范围和任务名；这些信息已经在总节点标题中体现。

角色名称映射：

| role id | role name |
|---------|-----------|
| role-cto | CTO / 技术决策者 |
| role-support | ZEGO 技术支持 |
| role-client-dev | 客户端开发 |
| role-server-dev | 服务端开发 |
| role-fullstack-dev | 全栈开发 |

未知 role id 使用文件名去掉 `.md` 作为标题。

## manifest 结构

脚本或手动创建后，必须写出：

```json
{
  "runName": "{run-name}",
  "folder": {
    "nodeToken": "...",
    "url": "..."
  },
  "documents": {
    "build-test-report": {
      "title": "...",
      "docId": "...",
      "url": "..."
    },
    "doc-eval-summary": {
      "title": "...",
      "docId": "...",
      "url": "..."
    },
    "doc-eval-role": {
      "role-client-dev": {
        "title": "...",
        "docId": "...",
        "url": "..."
      }
    }
  }
}
```

## 创建命令要点

创建任务节点：

```bash
lark-cli wiki nodes create \
  --params '{"space_id":"7187666870011232257"}' \
  --data '{"parent_node_token":"Bvy6wsTvjiLh7bkzOxVcwvyunTH","node_type":"origin","obj_type":"docx","title":"【{date} {product}-{platform}-{scope} 接入测试】"}' \
  --as user
```

创建文档骨架：

```bash
lark-cli docs +create --api-version v2 \
  --parent-token {folder_node_token} \
  --doc-format markdown \
  --content "$(cat <<'EOF'
# {报告标题}

> 报告骨架已创建，内容待写入。
EOF
)"
```

覆盖写入本地 Markdown：

```bash
bash .claude/skills/report-doc-test-in-feishu/scripts/write-feishu-markdown.sh \
  --doc-id "{document_id}" \
  --file "{local_markdown_file}"
```

底层仍然是 `lark-cli docs +update --command overwrite`。`--content` 是字符串，不是文件路径；脚本负责读取本地 Markdown 文件并传入内容。
