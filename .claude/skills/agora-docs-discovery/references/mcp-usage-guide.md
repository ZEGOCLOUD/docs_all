# Agora MCP 工具使用指南

## 服务器信息

- **URL**: `https://doc-mcp.shengwang.cn/mcp`
- **协议**: SSE (Server-Sent Events)
- **文档数量**: 8033+ 篇
- **GitHub**: https://github.com/Shengwang-Community/doc-mcp-server

---

## 三个工具

### 1. `search-docs` — 搜索文档

根据关键词搜索相关文档，返回匹配结果列表。

**请求**：
```json
{ "query": "rtc" }
```

**响应**：
```json
{
  "data": [
    {
      "text": "流程总览",
      "category": "default",
      "uri": "docs://default/analytics/general/rtc/call-search/overview"
    }
  ]
}
```

**使用建议**：
- 使用产品关键词：`rtc`, `signaling`, `whiteboard`, `chat`
- 使用中英文混合：`rtc 集成`, `signaling 消息`
- 使用具体功能：`混流`, `录制`, `推流`, `美颜`
- 搜索结果是摘要，需用 `get-doc-content` 获取完整内容

---

### 2. `list-docs` — 列出文档

获取所有文档的分类和列表。

**请求**：无参数

**响应**：
```json
{
  "categories": ["shared", "default", "api-reference", "faq", "basics"],
  "total": 8033,
  "docs": [
    {
      "path": "doc/rtm2/android/user-guide/setup/account-and-billing",
      "name": "account-and-billing",
      "category": "default",
      "depth": 6,
      "uri": "docs://default/rtm2/android/user-guide/setup/account-and-billing",
      "localPath": "default/rtm2/android/user-guide/setup/account-and-billing"
    }
  ]
}
```

**文档分类**：
| 分类 | 说明 |
|---|---|
| `default` | 产品文档（使用指南、集成教程等） |
| `api-reference` | API 参考文档 |
| `faq` | 常见问题 |
| `basics` | 基础概念 |
| `shared` | 共享文档 |

**URI 格式**：`docs://{category}/{product}/{platform}/{section}/{topic}`

---

### 3. `get-doc-content` — 获取文档内容

根据 URI 获取文档的完整内容。

**请求**：
```json
{ "uri": "docs://default/analytics/general/rtc/call-search/call-detail" }
```

**响应**：
```markdown
---
title: 查看通话详情
ag_product: analytics
ag_platform: general
---
本文介绍如何查看通话详情页面的三个子页面。
## 通话详情主页
...
```

**使用建议**：
- 先用 `search-docs` 获取 uri，再用此工具获取内容
- 响应包含 frontmatter 元数据（产品、平台、更新日期等）
- 内容为 Markdown 格式，可直接解析

---

## 典型查询流程

### 查询 Agora 白板功能

```
1. search-docs({ query: "whiteboard" })
   → 返回白板相关文档列表

2. 从结果中选择目标文档的 uri

3. get-doc-content({ uri: "docs://default/..." })
   → 获取完整文档内容
```

### 查询 Agora RTC 混流

```
1. search-docs({ query: "rtc 混流" })
   → 返回混流相关文档列表

2. get-doc-content({ uri: "docs://default/..." })
   → 获取完整文档内容
```

### 浏览 Agora Signaling 所有文档

```
1. search-docs({ query: "signaling" })
   → 返回 Signaling 相关文档列表

2. 逐个获取感兴趣的文档内容
```

---

## 配置方式

在项目的 `.claude/settings.json` 或全局配置中添加 MCP 服务器：

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

或使用 CLI 添加：
```bash
claude mcp add --transport http shengwang-docs https://doc-mcp.shengwang.cn/mcp
```
