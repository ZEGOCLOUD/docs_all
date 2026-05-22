# 示例输出格式

## 场景一：查询 Agora RTC 功能

**输入**：`Agora RTC 的混流功能有哪些`

**操作**：search-docs("rtc 混流") → get-doc-content(uri)

**输出**：

```markdown
## Agora RTC 混流功能

- 产品：Agora RTC
- 对应 ZEGO 产品：Express Video
- 查询方式：Agora MCP search-docs

### 核心能力
- [从 MCP 文档内容提取]

### ZEGO vs Agora 对比
| 功能 | ZEGO Express | Agora RTC |
|---|---|---|
| [功能对比] | [ZEGO 支持情况] | [Agora 支持情况] |
```

---

## 场景二：查询 Agora 白板能力

**输入**：`声网白板支持像素级擦除吗`

**操作**：search-docs("whiteboard 擦除") → get-doc-content(uri)

**输出**：

```markdown
## Agora Interactive Whiteboard 擦除能力

- 产品：Interactive Whiteboard
- 对应 ZEGO 产品：Super Board
- 查询方式：Agora MCP search-docs

### 擦除功能
- [从 MCP 文档内容提取]

### ZEGO vs Agora 对比
| 功能 | ZEGO Super Board | Agora Whiteboard |
|---|---|---|
| 整页擦除 | 支持 | [从文档确认] |
| 像素级擦除 | 不支持 | [从文档确认] |
| 分段擦除 | 支持 | [从文档确认] |
```

---

## 场景三：查询 Agora Signaling 集成

**输入**：`声网 Signaling 怎么集成`

**操作**：search-docs("signaling 集成") → get-doc-content(uri)

**输出**：

```markdown
## Agora Signaling 集成指南

- 产品：Agora Signaling
- 对应 ZEGO 产品：ZIM
- 查询方式：Agora MCP search-docs

### 集成步骤
1. [从 MCP 文档内容提取]
2. ...

### 相关 API
- [从 MCP 文档内容提取]
```

---

## 场景四：列出所有竞品

**输入**：`列出所有声网竞品及其文档查询方式`

**输出**：

```markdown
## 声网 Agora 竞品文档查询方式一览

所有产品使用 Agora MCP 服务器查询文档。

| ZEGO 产品 | Agora 产品 | MCP 搜索关键词 |
|---|---|---|
| Express Video/Audio | Agora RTC | rtc, voice-calling, video-calling |
| ZIM | Agora Signaling | signaling, rtm, rtm2 |
| ZIM | Agora Chat | chat, im, 即时通讯 |
| LFL | Interactive Live Streaming | live-streaming, 互动直播 |
| Cloud Recording | Cloud Recording | cloud-recording, 录制 |
| Call Kit | Agora Call Kit | call-kit |
| Live Streaming Kit | Live Streaming Kit | live-streaming-kit |
| Video Conference Kit | Video Conference Kit | video-conference-kit |
| IMKit | Chat UIKit | chat-uikit, uikit |
| AI Effects | AI Effects | ai-effects, 美颜 |
| Super Board | Interactive Whiteboard | whiteboard, 白板 |
```

---

## 场景五：功能对比分析

**输入**：`对比 ZEGO 和 Agora 的即时通讯能力`

**操作**：search-docs("chat") + search-docs("signaling") → get-doc-content(uri)

**输出**：

```markdown
## ZEGO vs Agora 即时通讯对比

### 产品映射
- ZEGO ZIM → Agora Signaling + Agora Chat
- 注意：Agora 将消息拆分为两个产品

### 功能对比
| 功能 | ZEGO ZIM | Agora Signaling | Agora Chat |
|---|---|---|---|
| 单聊 | 支持 | 支持 | 支持 |
| 群聊 | 支持 | 支持（频道消息） | 支持 |
| 离线消息 | 支持 | [从文档确认] | [从文档确认] |
| 消息回执 | 支持 | [从文档确认] | [从文档确认] |

### 差异点
- [从 MCP 文档内容提取关键差异]
```
