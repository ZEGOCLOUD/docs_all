# 附件打包和上传

附件上传使用脚本完成，不手写一串 zip 和 media-insert 命令。脚本会：

1. 清理并压缩源码目录。
2. 按传入路径压缩自动化运行报告目录，例如 `midscene_run`。
3. 上传源码包和自动化运行报告包到构建与自动化测试报告文档。
4. 插入截图目录下的图片。

`lark-cli docs +media-insert --file` 只接受当前目录内的相对路径；脚本内部会自动进入文件所在目录并传入 `./filename`，调用方可以传相对路径或绝对路径。

## 使用脚本

必填参数：

- `--doc-id`: 构建与自动化测试报告飞书文档 ID。
- `--run-dir`: 本次 run 目录。
- `--demo-dir`: 示例源码目录。

构建与自动化测试报告必填参数：

- `--midscene-run-dir`: 自动化测试工具生成的运行报告目录，例如 `doc-test-reports/{run-name}/examples/{demo-name}/midscene_run` 或其它实际路径。不传或目录不存在时跳过。
- `--screenshot-dir`: 截图目录，例如 `doc-test-reports/{run-name}/auto-test/screenshots`。不传或目录不存在时跳过。

```bash
bash .claude/skills/report-doc-test-in-feishu/scripts/upload-feishu-report-assets.sh \
  --doc-id "{build_test_report_doc_id}" \
  --run-dir "doc-test-reports/{run-name}" \
  --demo-dir "doc-test-reports/{run-name}/examples/{demo-name}" \
  --midscene-run-dir "{midscene_run_dir}" \
  --screenshot-dir "doc-test-reports/{run-name}/auto-test/screenshots"
```

## 输出文件

脚本会在 `--run-dir` 下生成：

```text
source-{demo-name}.zip
midscene-run.zip   # 仅在 --midscene-run-dir 存在时生成
```

自动化测试运行报告目录不固定，先在 run 目录下发现实际 `midscene_run` 路径，再通过 `--midscene-run-dir` 明确传入。不要默认压缩整个 `auto-test/` 目录。
