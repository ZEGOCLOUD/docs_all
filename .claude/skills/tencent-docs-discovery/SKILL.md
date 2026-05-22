---
name: tencent-docs-discovery
description: 腾讯云竞品文档发现与读取指南。使用浏览器自动化读取腾讯云文档。触发词："腾讯云文档", "竞品文档", "TRTC 文档", "腾讯 IM", "腾讯云产品", "tencent docs", "读取腾讯云", "腾讯特效", "腾讯直播", "腾讯白板", "腾讯数字人", "竞品分析"。
---

# 腾讯云文档发现与读取

使用浏览器自动化（Playwright）读取腾讯云产品文档。统一方案，所有产品通用。

## 第零步：确保浏览器自动化工具可用

本 skill 依赖 Playwright 浏览器自动化 MCP 工具（`browser_navigate`、`browser_snapshot`、`browser_click` 等）。

1. 检查当前环境是否有 `browser_navigate` 等 Playwright MCP 工具
2. 如果没有，需先配置 Playwright MCP 服务器后才能使用本 skill
3. 腾讯云无官方 MCP 服务器，浏览器自动化是唯一方案，**无法降级到 Web Search**

## 第一步：定位产品

读取 `references/tencent-mapping.md`，查找 ZEGO 产品对应的腾讯云产品及其产品 ID。

## 第二步：浏览器自动化读取文档

### 操作流程

1. `browser_navigate` → 打开产品总览页 `https://cloud.tencent.com/document/product/{产品ID}`
2. `browser_snapshot` → 获取页面无障碍树快照（含左侧目录结构和链接）
3. `browser_click` → 点击目标章节，导航到子文档
4. `browser_snapshot` → 提取子文档内容

### 为什么用浏览器自动化

- **保留完整链接信息**，可提取子文档的 URL（Web Reader 会剥离 href）
- **可点击左侧目录**导航到子页面，实现逐章阅读
- **可获取完整 DOM 结构**和表格数据
- **可截图**辅助理解页面布局

## 第三步：输出结果

根据用户需求输出，详见 `references/example-outputs.md`。

## 常用场景速查

| 场景 | 操作 |
|---|---|
| "TRTC 的混流功能" | 浏览器自动化打开 647 总览页 → 快照提取目录 → 点击「云端混流转码」章节 |
| "腾讯 IM 群组类型" | 浏览器自动化打开 269 总览页 → 快照提取目录 → 点击「群组管理」章节 |
| "TUICallKit 怎么集成" | 浏览器自动化打开 647 总览页 → 快照提取目录 → 点击 TUICallKit 相关章节 |
| "腾讯直播 CDN 推流" | 浏览器自动化打开 267 总览页 → 快照提取目录 → 点击「CDN 推流」章节 |
| "腾讯云白板能力" | 浏览器自动化打开 1137 总览页 → 快照提取目录 → 点击「开发指南」章节 |
| "腾讯特效 SDK 美颜" | 浏览器自动化打开 616 总览页 → 快照提取目录 → 点击「美颜」章节 |
| "智能数智人文档" | 浏览器自动化打开 1240 总览页 → 快照提取目录 → 点击目标章节 |

## 参考资源

| 文件 | 用途 |
|---|---|
| `references/tencent-mapping.md` | ZEGO → 腾讯云产品映射表（产品 ID、URL、目录结构） |
| `references/browser-automation-guide.md` | 浏览器自动化操作指南 |
| `references/example-outputs.md` | 各种场景的输出格式示例 |
