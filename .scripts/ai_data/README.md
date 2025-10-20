# ai_data 使用说明（已按最新流程更新）

## 环境变量（.scripts/ai_data/.env）
在本目录下创建 .env 并填入：
- RAGFLOW_BASE_URL=https://ai-service2.zegocloud.com/api/v1
- RAGFLOW_API_KEY=ragflow-xxxx
- RUN_COMPLETED_NOTE_FEISHU_WEBHOOK=https://open.feishu.cn/open-apis/bot/v2/hook/...

说明：脚本会自动读取同目录 .env（只填充缺失的环境变量）。

## 运行更新
- 普通模式（交互选择产品组→实例，不再询问下载模式）
  - ./run_update_ai_data.sh
- 全量模式（每周批量，逐个实例 下载→更新知识库→删除本地文件）
  - ./run_update_ai_data.sh --all
  - 特性：
    - 遍历所有产品的所有实例
    - 每处理完一个实例即清理该实例本地 md 文件，避免占用空间/触发 CI 限制
    - 自动跳过以下实例（内容重复）：real_time_voice_zh、live_streaming_zh
    - 运行结束自动汇总并通过飞书机器人发送摘要（若设置了 RUN_COMPLETED_NOTE_FEISHU_WEBHOOK）

## 定时任务（Linux）
- 管理脚本：.scripts/ai_data/schedule_ai_data.sh
- 用法：
  - 交互：./schedule_ai_data.sh，然后按提示输入
    - 回车 或 1：启动定时任务（每周六 02:00 执行 ./run_update_ai_data.sh --all）
    - 2：停止定时任务
  - 直接命令：
    - ./schedule_ai_data.sh start
    - ./schedule_ai_data.sh stop
- 日志：.scripts/ai_data/logs/ai_data_cron.log

## 清理知识库工具
- 删除 document_count=0 的知识库（默认）：
  - python .scripts/ai_data/cleanup_datasets.py
- 预览将删除哪些（不执行）：
  - python .scripts/ai_data/cleanup_datasets.py --dry-run
- 删除所有知识库（危险，分批删除，避免超时）：
  - python .scripts/ai_data/cleanup_datasets.py --all

## 其他说明
- 已移除 crawl4ai 与 Playwright 依赖检查与安装；无需这两个依赖
- 语言固定为中文（英文 sitemap 逻辑保留但默认不启用）
- 下载：直接请求 sitemap 匹配到的 .md 链接
- 文件名：从 Markdown 标题提取（自动清理 <...> 标签），并拼接实例名，避免过长/异常
- RagFlow：创建/更新 Dataset 时，按文档要求构造请求体（已去除 language；chunk_token_num 为整数）
