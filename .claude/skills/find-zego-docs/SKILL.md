---
name: find-zego-docs
description: This skill should be used when you need to find or read ZEGO technical documentation in the docs repository. Provides product-platform-to-path mapping, search strategies, and reading priorities. Triggers on "查找文档", "find docs", "查阅文档", "找文档", "文档路径", "search docs", "read docs", "搜索文档", "doc path".
---

# ZEGO 文档查找

根据产品和平台在文档仓库中定位相关技术文档，按优先级读取。

## 查找流程

### 第一步：定位路径

读取 `references/products-platforms.md`，从表格中查找目标产品和平台对应的 `文档路径`。

示例：实时音视频 + Android Java → `core_products/real-time-voice-video/zh/android-java`

### 第二步：按需查找和读取

根据你需要的信息类型，选择对应的查找策略：

| 我需要 | 查找方式 | 注意事项 |
|-------|---------|---------|
| 如何引入 SDK | 在文档路径下找 `integration` 相关 .mdx | 集成指南通常在文档路径的根或一级子目录 |
| 最小可用示例 | 在文档路径下找 `quick-start` 相关 .mdx | 快速开始通常包含完整的初始化→加入房间→推拉流流程 |
| 具体接口说明 | 在 `client-sdk/api-reference` 下找 .mdx | API 文档通常很大（数千行），**必须先用 Grep 定位到目标方法的行号，再用 Read 的 offset/limit 读取附近内容**，不要整文件读取 |
| 服务端接口 | 在文档路径下找 `server` 目录下的 .yaml | 优先读 yaml；如果没有 yaml 再读 .mdx |
| Token 鉴权 | 在文档路径下搜索 `Token` 相关 .mdx | Token 文档通常包含生成算法和参数说明 |
| 特定功能实现 | Grep 关键词 + 平台路径限定 | 如 `Grep "混流" core_products/real-time-voice-video/zh/android-java/` |

## 注意事项

- **相同平台不同语言的可以都读取** — 确认路径中的平台标识符（`android-java` and `android-kotlin`）后，可以都读取
- **API 文档禁止整文件读取** — 动辄数千行，会浪费大量 context window
- **服务端 API 优先 yaml** — yaml 格式结构更清晰，信息密度更高
- **多个文档可并行读取** — 如果需要同时查阅集成指南和 API 文档，并行 Read 节省时间

## 参考资源

| 文件 | 用途 |
|-----|------|
| `references/products-platforms.md` | 所有产品的平台列表和文档路径映射 |
