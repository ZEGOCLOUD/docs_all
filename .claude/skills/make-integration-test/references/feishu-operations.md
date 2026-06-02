# 飞书文档操作规范

## 任务文件夹创建

在飞书知识库的「接入测试」节点下创建本次评测的文件夹。

父节点信息：
- space_id: `7187666870011232257`
- parent_node_token: `Bvy6wsTvjiLh7bkzOxVcwvyunTH`

```bash
lark-cli wiki nodes create --params '{"space_id":"7187666870011232257"}' --data '{"parent_node_token":"Bvy6wsTvjiLh7bkzOxVcwvyunTH","node_type":"origin","obj_type":"docx","title":"【日期 产品名-文档类型 接入测试】"}' --as user
```

注意：`space_id` 是 path 参数，必须用 `--params` 传；body 参数用 `--data` 传。两者分开。

记录返回的 node_token，后续文档都在这个节点下创建。

## 文档创建与写入

分两步操作：

### Step A: 创建空文档

在任务文件夹下创建：

```bash
lark-cli docs +create --api-version v2 --parent-token {folder_node_token} --doc-format markdown --content "$(cat <<'EOF'
# 【角色名】评测报告
EOF
)"
```

### Step B: 用 overwrite 写入完整内容

`--content` 接收字符串，不是文件路径：

```bash
lark-cli docs +update --api-version v2 --doc {document_id} --command overwrite --doc-format markdown --content "$(cat <<'EOF'
# 【角色名】评测报告
... 完整报告 markdown 内容 ...
EOF
)"
```

### 关键注意事项

- `--content` 直接接收字符串内容，**不能**用 `@-`（stdin）或 `@file.md`（文件路径）
- 内容较长时用 `$(cat <<'EOF' ... EOF)` heredoc 包裹
- `docs +create` 的 `--content` 参数必填，不能为空
- 长文档可先 `+create` 建骨架，再用 `+update --command append` 分段追加
- overwrite 内容的第一行必须是 `# 标题`

## 常用操作速查

| 操作 | 命令 |
|------|------|
| 创建文件夹 | `lark-cli wiki nodes create --params '{"space_id":"..."}' --data '{"parent_node_token":"...","node_type":"origin","obj_type":"docx","title":"..."}' --as user` |
| 创建文档 | `lark-cli docs +create --api-version v2 --parent-token {token} --doc-format markdown --content "# 标题"` |
| 覆盖写入 | `lark-cli docs +update --api-version v2 --doc {doc_id} --command overwrite --doc-format markdown --content "$(cat <<'EOF' ... EOF)"` |
| 追加内容 | `lark-cli docs +update --api-version v2 --doc {doc_id} --command append --doc-format markdown --content "$(cat <<'EOF' ... EOF)"` |
| 上传文件附件 | `lark-cli docs +media-insert --doc {doc_id} --file ./report.zip --type file` |
| 插入截图 | `lark-cli docs +media-insert --doc {doc_id} --file ./screenshots/step1.png --type image --caption "步骤1截图"` |

## 上传测试报告和截图

### 打包自动化测试报告为 zip

包含测试用例、测试脚本、截图和 midscene 运行报告：

```bash
cd examples/{项目名}
zip -r test-report.zip test-cases.md test-cases.sh screenshots/ midscene_run/
```

### 上传 zip 到飞书文档

使用 `docs +media-insert --type file` 上传附件，会以卡片形式嵌入文档末尾：

```bash
lark-cli docs +media-insert --doc {document_id} --file ./examples/{项目名}/test-report.zip --type file
```

`--file-view` 可选参数控制附件展示形式：
- `card`（默认）：文件卡片
- `preview`：音视频内联播放器
- `inline`：内联展示

### 逐张插入截图

截图目录下的每张图片逐个插入到飞书文档的"自动化测试"章节下：

```bash
# 先找到"自动化测试"章节的 block_id
lark-cli docs +fetch --api-version v2 --doc {document_id} --detail with-ids --scope outline

# 在目标 block 后插入截图
lark-cli docs +media-insert --doc {document_id} --file ./screenshots/tc01-login.png --type image --caption "TC-01 登录成功"
lark-cli docs +media-insert --doc {document_id} --file ./screenshots/tc02-send.png --type image --caption "TC-02 发送消息"
```

也可以用 `--selection-with-ellipsis` 定位插入位置：

```bash
lark-cli docs +media-insert --doc {document_id} \
  --file ./screenshots/tc01-login.png --type image --caption "TC-01" \
  --selection-with-ellipsis "自动化测试截图"
```

### 批量插入截图脚本示例

```bash
DOC_ID={document_id}
SCREENSHOT_DIR=./examples/{项目名}/screenshots

# 先插入分隔标题
lark-cli docs +update --api-version v2 --doc $DOC_ID --command append \
  --doc-format markdown --content "## 测试截图"

# 遍历截图目录插入每张图片
for img in "$SCREENSHOT_DIR"/*.png; do
  filename=$(basename "$img" .png)
  echo "插入截图: $filename"
  lark-cli docs +media-insert --doc $DOC_ID --file "$img" --type image --caption "$filename"
done
```
