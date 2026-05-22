---
name: agora-docs-discovery
description: 声网 Agora 竞品文档发现与查询指南。使用 Agora 官方 MCP 服务器查询文档。触发词："Agora文档", "声网文档", "Agora RTC", "Agora Signaling", "Agora Chat", "声网白板", "声网录制", "竞品分析", "agora docs", "agora competitive"。
---

# 声网 Agora 文档发现

使用 Agora 官方 MCP 服务器查询声网产品文档。Agora 提供官方 MCP 服务，覆盖 8000+ 篇文档，无需浏览器自动化。

## 第零步：检查并确保 MCP 服务器已配置

本 skill 的核心能力依赖 Agora MCP 服务器。**在执行后续步骤前，必须先确认 MCP 服务器可用。**

1. 检查当前环境是否有 `search-docs`、`get-doc-content` 等 MCP 工具可用
2. 如果没有，按照 `references/mcp-usage-guide.md` 中的「配置方式」章节，将 MCP 服务器添加到项目的 `.claude/settings.json` 中：
   ```json
   {
     "mcpServers": {
       "shengwang-docs": {
         "url": "https://doc-mcp.shengwang.cn/mcp",
         "type": "sse"
       }
     }
   }
   ```
3. 配置后需要重启 Claude Code 会话才能生效
4. **只有在 MCP 工具不可用且无法立即配置的情况下**，才降级使用 Web Search + Web Reader 作为替代方案

## 第一步：定位产品

读取 `references/agora-mapping.md`，查找 ZEGO 产品对应的 Agora 产品和 MCP 查询关键词。

## 第二步：MCP 查询文档

使用 Agora MCP 服务器工具（需在项目中配置 MCP Server，详见 `references/mcp-usage-guide.md`）：

1. **`search-docs`** — 用关键词搜索相关文档，返回匹配文档列表（含 uri）
2. **`get-doc-content`** — 根据 uri 获取文档完整内容

### 为什么用 MCP

- **官方维护**，数据准确、实时更新
- **结构化数据**，直接返回文档内容，无需解析 HTML
- **快速高效**，无需浏览器加载页面
- **覆盖全面**，8000+ 篇文档，涵盖所有 Agora 产品

## 第三步：输出结果

根据用户需求输出，详见 `references/example-outputs.md`。

## 常用场景速查

| 场景 | 操作 |
|---|---|
| "Agora RTC 混流功能" | search-docs("rtc 混流") → get-doc-content(uri) |
| "声网白板能力" | search-docs("whiteboard") → get-doc-content(uri) |
| "Agora Signaling 集成" | search-docs("signaling 集成") → get-doc-content(uri) |
| "声网云端录制" | search-docs("cloud-recording") → get-doc-content(uri) |
| "Agora Chat 群组" | search-docs("chat 群组") → get-doc-content(uri) |
| "Agora Call Kit" | search-docs("call-kit") → get-doc-content(uri) |
| "Agora 美颜特效" | search-docs("ai-effects") → get-doc-content(uri) |

## 参考资源

| 文件 | 用途 |
|---|---|
| `references/agora-mapping.md` | ZEGO → Agora 产品映射表（查询关键词） |
| `references/mcp-usage-guide.md` | Agora MCP 工具使用指南 |
| `references/example-outputs.md` | 各种场景的输出格式示例 |
