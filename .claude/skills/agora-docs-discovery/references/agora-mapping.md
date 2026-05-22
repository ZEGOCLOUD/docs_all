# ZEGO → 声网 Agora 产品映射表

本文件维护 ZEGO 产品与声网 Agora 对应产品的映射关系。所有产品使用 Agora MCP 服务器查询文档。

数据来源：ZEGO https://doc-zh.zego.im/ | Agora https://doc.shengwang.cn/

---

## MCP 服务器配置

- **URL**: `https://doc-mcp.shengwang.cn/mcp`
- **工具**: `search-docs`（搜索）、`list-docs`（列表）、`get-doc-content`（内容）

---

## 一、互动核心产品

### 1. 实时音视频 (Express Video) → 实时互动 RTC

| 字段 | 值 |
|---|---|
| Agora 产品名 | 实时互动 RTC |
| MCP 关键词 | `rtc`, `实时音视频`, `音视频`, `voice-calling`, `video-calling` |

### 2. 实时语音 (Express Audio) → 实时互动 RTC（语音模式）

| 字段 | 值 |
|---|---|
| Agora 产品名 | 实时互动 RTC（纯语音场景） |
| MCP 关键词 | `rtc`, `语音通话`, `voice` |
| 备注 | Agora 无独立语音产品，RTC SDK 统一覆盖 |

### 3. 超低延迟直播 (LFL) → 融合 CDN 直播

| 字段 | 值 |
|---|---|
| Agora 产品名 | 融合 CDN 直播 |
| MCP 关键词 | `cdn`, `直播`, `融合cdn`, `推流`, `旁路推流` |

### 4. 即时通讯 (ZIM) → 即时通讯 IM + 实时消息 RTM

ZIM 对应 Agora **两个产品**，查询时需分别搜索：

**4a. 实时消息 RTM（低延迟消息通道）**

| 字段 | 值 |
|---|---|
| Agora 产品名 | 实时消息 RTM（云信令） |
| MCP 关键词 | `rtm`, `rtm2`, `signaling`, `信令`, `实时消息` |

**4b. 即时通讯 IM（聊天体系）**

| 字段 | 值 |
|---|---|
| Agora 产品名 | 即时通讯 IM |
| MCP 关键词 | `chat`, `im`, `即时通讯`, `群组`, `聊天`, `聊天室` |

---

## 二、AIGC

### 5. 实时互动 AI Agent → 对话式 AI 引擎

| 字段 | 值 |
|---|---|
| Agora 产品名 | 对话式 AI 引擎（NEW/HOT） |
| MCP 关键词 | `conversational-ai`, `对话式AI`, `ai agent`, `ai引擎` |
| 备注 | Agora 无独立 AI Agent 产品名，使用"对话式 AI 引擎" |

### 6. 数字人 API → 无直接对应

| 字段 | 值 |
|---|---|
| Agora 对应 | 无独立数字人产品 |
| 替代方案 | 可通过对话式 AI 引擎 + RTC 实现 |
| MCP 关键词 | `conversational-ai`, `数字人`, `avatar` |

---

## 三、互动扩展服务

### 7. 超级白板 (Super Board) → 互动白板

| 字段 | 值 |
|---|---|
| Agora 产品名 | 互动白板（Whiteboard SDK / Fastboard SDK） |
| MCP 关键词 | `whiteboard`, `白板`, `互动白板`, `fastboard` |

### 8. 云端播放器 → 输入在线媒体流

| 字段 | 值 |
|---|---|
| Agora 产品名 | 输入在线媒体流（媒体服务子功能） |
| MCP 关键词 | `输入在线媒体流`, `inject stream`, `媒体流输入` |

### 9. AI 美颜 → SDK 拓展插件

| 字段 | 值 |
|---|---|
| Agora 产品名 | SDK 拓展插件（含 AI 美颜、虚拟背景等） |
| MCP 关键词 | `美颜`, `ai-effects`, `虚拟背景`, `特效`, `extension`, `sdk拓展` |
| 备注 | Agora 将美颜等作为 SDK 拓展插件，非独立产品 |

### 10. 云端录制 → 云端录制

| 字段 | 值 |
|---|---|
| Agora 产品名 | 云端录制（媒体服务子功能） |
| MCP 关键词 | `cloud-recording`, `云端录制`, `录制` |

### 11. 本地服务端录制 → 本地服务端录制

| 字段 | 值 |
|---|---|
| Agora 产品名 | 本地服务端录制（媒体服务子功能） |
| MCP 关键词 | `on-premise-recording`, `本地录制`, `服务端录制` |

### 12. 星图 → 水晶球

| 字段 | 值 |
|---|---|
| Agora 产品名 | 水晶球（全周期通话质量检测、回溯和分析方案） |
| MCP 关键词 | `水晶球`, `analytics`, `质量`, `通话质量` |

### 13. 云端实时语音识别 → 实时转录翻译

| 字段 | 值 |
|---|---|
| Agora 产品名 | 实时转录翻译（NEW） |
| MCP 关键词 | `转录`, `翻译`, `stt`, `语音识别`, `实时转录`, `real-time-stt` |

---

## 四、UIKits

ZEGO UIKit 在 Agora 中**无直接对应的独立 UIKit 产品**。Agora 的低代码方案是灵动课堂/灵动会议，属于 aPaaS 层级。

| ZEGO UIKit | Agora 近似对应 | MCP 关键词 | 备注 |
|---|---|---|---|
| 音视频通话 UIKit | 灵动会议 / 对话式 AI 引擎 | `灵动会议`, `meeting` | Agora 无独立 Call Kit UIKit |
| 互动直播 UIKit | 无直接对应 | `直播`, `live-streaming` | 需用 RTC SDK 自行实现 |
| 语聊房 UIKit | 无直接对应 | `语聊`, `chatroom` | 需用 RTC + RTM 自行实现 |
| IMKit | 无直接对应 | `chat`, `uikit` | Agora IM 无独立 UIKit |

---

## 五、云市场

### 14. 数美内容审核 → 云市场（内容审核）

| 字段 | 值 |
|---|---|
| Agora 产品名 | 云市场（集成第三方内容审核服务） |
| MCP 关键词 | `云市场`, `内容审核`, `moderation` |

### 15. 大饼 AI 变声 → SDK 拓展插件（变声）

| 字段 | 值 |
|---|---|
| Agora 产品名 | SDK 拓展插件（音频特效/变声） |
| MCP 关键词 | `变声`, `voice-changer`, `音频特效`, `extension` |
| 备注 | Agora 变声能力在 SDK 拓展插件或 RTC 内置音频特效中 |

### 16. 实时传译 → 实时转录翻译

| 字段 | 值 |
|---|---|
| Agora 产品名 | 实时转录翻译（NEW） |
| MCP 关键词 | `翻译`, `传译`, `实时转录`, `real-time-stt` |

---

## 六、媒体服务与能力（分属不同产品线的子功能）

以下能力 Agora 列为独立产品/子产品，ZEGO 分布在对应产品线中：

### 21. 微呼叫/小程序互通 → Express Video 小程序端

| 字段 | 值 |
|---|---|
| ZEGO 位置 | Express Video → 小程序端（`mini-program`） |
| Agora 产品 | 微呼叫（NEW） |
| MCP 关键词 | `微呼叫`, `miniprogram`, `小程序` |

### 22. PPT 转码 → 超级白板文件转换

| 字段 | 值 |
|---|---|
| ZEGO 位置 | 超级白板 → 文件管理（支持 PPT/PPTX/DOC 转图片/网页） |
| Agora 产品 | PPT 转码服务（独立产品） |
| MCP 关键词 | `ppt转码`, `文档转换`, `文件转换` |

### 23. RTC 服务端 SDK → Express Video 服务端 API

| 字段 | 值 |
|---|---|
| ZEGO 位置 | Express Video → 服务端（`server`） |
| Agora 产品 | RTC 服务端 SDK（独立产品） |
| MCP 关键词 | `rtc-server-sdk`, `服务端sdk` |

### 24. 旁路推流 → Express Video CDN直播 + LFL CDN推流

| 字段 | 值 |
|---|---|
| ZEGO 位置 | Express Video → CDN 直播 / LFL → OBS推流 |
| Agora 产品 | 旁路推流（媒体服务子功能） |
| MCP 关键词 | `旁路推流`, `cdn`, `推流`, `cdn-live` |

### 25. 云端转码/混流 → Express Video 混流

| 字段 | 值 |
|---|---|
| ZEGO 位置 | Express Video → 直播场景 → 混流（`stream-mixing`） |
| Agora 产品 | 云端转码（媒体服务子功能） |
| MCP 关键词 | `云端转码`, `混流`, `transcode`, `mix` |

### 26. RTMP 网关 → Express Video RTMP拉流

| 字段 | 值 |
|---|---|
| ZEGO 位置 | Express Video → 支持通过 URL 拉取 RTMP 流 |
| Agora 产品 | RTMP 网关（媒体服务子功能） |
| MCP 关键词 | `rtmp`, `网关`, `拉流` |

### 27. 灵动课堂（Legacy）→ 大班课/小班课/AI大班课

| 字段 | 值 |
|---|---|
| ZEGO 位置 | 解决方案 → 大班课、小班课、AI大班课（数字人伴学） |
| Agora 产品 | 灵动课堂（**Legacy**，已移至 Legacy 产品区） |
| MCP 关键词 | `flexible-classroom`, `灵动课堂`, `教育` |
| 备注 | 2025 年声网将灵动课堂移至 Legacy，教育方案改用场景化解决方案（一对一互动教学、一对多互动教学、超级小班课等） |

### 28. 灵动会议 → 视频会议方案

| 字段 | 值 |
|---|---|
| ZEGO 位置 | 解决方案 → 视频会议 |
| Agora 产品 | 灵动会议（NEW，低代码平台） |
| MCP 关键词 | `灵动会议`, `meeting`, `视频会议` |

### 29. Status Page → ZEGO 服务可用性协议（非产品）

| 字段 | 值 |
|---|---|
| ZEGO 位置 | 通用文档 → 服务可用性保障（SLA 协议文档） |
| Agora 产品 | Status Page（NEW，公开状态页） |
| MCP 关键词 | `status`, `服务状态`, `可用性` |
| 备注 | ZEGO 无公开 Status Page，仅有 SLA 协议文档 |

### 30. 媒体流加速 RTSA → Express Video 硬件接入

| 字段 | 值 |
|---|---|
| ZEGO 位置 | Express Video → 支持 Linux/嵌入式等硬件平台接入 |
| Agora 产品 | 媒体流加速 RTSA（独立产品） |
| MCP 关键词 | `rtsa`, `媒体流加速`, `硬件` |
| 备注 | ZEGO 无独立 RTSA 品牌，硬件接入能力在 Express Video 内 |

---

## 七、Agora 解决方案（对应 ZEGO 解决方案）

Agora 的解决方案分为社交娱乐、教育、IOT 三大方向：

### 社交娱乐

| ZEGO 方案 | Agora 方案 | MCP 关键词 | 备注 |
|---|---|---|---|
| 在线 KTV | 在线 K 歌房 | `k歌`, `karaoke` | Agora 独立场景方案 |
| 互动直播 | 秀场直播 | `秀场直播`, `直播` | Agora 有独立方案 |
| 语聊房 | 声动语聊 | `声动语聊`, `语聊` | Agora 特色方案 |
| 1v1 视频通话 | 1v1 私密房 | `1v1`, `私密房` | Agora 独立场景方案 |
| - | 游戏语音（NEW） | `游戏语音`, `game-voice` | Agora 新方案，ZEGO 无独立方案 |

### 教育

| ZEGO 方案 | Agora 方案 | MCP 关键词 | 备注 |
|---|---|---|---|
| 一对一教学 | 一对一互动教学 | `一对一`, `互动教学` | 直接对应 |
| 一对多教学 | 一对多互动教学 | `一对多`, `互动教学` | 直接对应 |
| 小班课 | 超级小班课 | `小班课`, `超级小班课` | Agora 命名不同 |
| 在线美术教学 | 在线美术教学 | `美术教学`, `美术` | 直接对应 |
| 在线音乐教学 | 在线音乐教学 | `音乐教学`, `音乐` | 直接对应 |
| 大班课 | 教育信息化 | `教育信息化`, `专递课堂` | Agora 归入教育信息化 |
| AI 大班课 | - | - | Agora 无对应，原灵动课堂已 Legacy |

### IOT（Agora 新方向）

| ZEGO 对应 | Agora 方案 | MCP 关键词 | 备注 |
|---|---|---|---|
| Express Video 硬件接入 | 对话式 AI 开发套件 | `ai开发套件`, `智能玩具` | Agora IOT 方案 |
| Express Video 硬件接入 | 智能门铃 | `智能门铃`, `门铃` | Agora IOT 方案 |
| Express Video 硬件接入 | 智能手表 | `智能手表`, `手表` | Agora IOT 方案 |
| Express Video 硬件接入 | 智能摄像头 | `智能摄像头` | Agora IOT 方案 |
| Express Video 硬件接入 | 平行操控 | `平行操控`, `远程操控` | Agora IOT 方案 |

---

## 八、Agora Legacy 产品

以下 Agora 产品已移至 Legacy 区，不再活跃开发：

| Agora Legacy 产品 | 原 ZEGO 对应 | 状态 |
|---|---|---|
| 语音通话（Legacy） | Express Audio | Legacy |
| 视频通话（Legacy） | Express Video | Legacy |
| 互动直播（Legacy） | LFL | Legacy |
| 极速直播（Legacy） | LFL | Legacy |
| 云信令（原实时消息） | ZIM | Legacy，已被 RTM 替代 |
| 灵动课堂（Legacy） | 大班课/小班课/AI大班课 | Legacy，教育方案改用场景化方案 |

---

## 总表

### ZEGO → Agora 完整映射

| # | ZEGO 产品 | Agora 对应产品 | MCP 关键词 | 已验证 |
|---|---|---|---|---|
| 1 | 实时音视频 | 实时互动 RTC | rtc, 音视频 | Y |
| 2 | 实时语音 | 实时互动 RTC（语音模式） | rtc, 语音 | Y |
| 3 | 超低延迟直播 | 融合 CDN 直播 | cdn, 直播, 旁路推流 | Y |
| 4 | 即时通讯 (ZIM) | 即时通讯 IM + 实时消息 RTM | chat, im, rtm, signaling | Y |
| 5 | 实时互动 AI Agent | 对话式 AI 引擎 | conversational-ai, ai agent | Y |
| 6 | 数字人 API | 对话式 AI 引擎（近似） | conversational-ai, avatar | Y |
| 7 | 超级白板 | 互动白板 | whiteboard, fastboard | Y |
| 8 | 云端播放器 | 输入在线媒体流 | inject stream, 媒体流输入 | Y |
| 9 | AI 美颜 | SDK 拓展插件 | 美颜, ai-effects, 虚拟背景 | Y |
| 10 | 云端录制 | 云端录制 | cloud-recording, 录制 | Y |
| 11 | 本地服务端录制 | 本地服务端录制 | on-premise-recording | Y |
| 12 | 星图 | 水晶球 | 水晶球, analytics, 质量 | Y |
| 13 | 云端实时语音识别 | 实时转录翻译 | 转录, stt, 语音识别 | Y |
| 14 | 音视频通话 UIKit | 灵动会议（近似） | 灵动会议, meeting | Y |
| 15 | 互动直播 UIKit | 无独立对应（需 RTC 自建） | 直播, live-streaming | Y |
| 16 | 语聊房 UIKit | 无独立对应（需 RTC+RTM 自建） | 语聊, chatroom | Y |
| 17 | IMKit | 无独立对应 | chat, uikit | Y |
| 18 | 数美内容审核 | 云市场（内容审核） | 云市场, 内容审核 | Y |
| 19 | 大饼 AI 变声 | SDK 拓展插件 | 变声, voice-changer | Y |
| 20 | 实时传译 | 实时转录翻译 | 翻译, 传译, stt | Y |
| 21 | 小程序互通 | 微呼叫 | 微呼叫, miniprogram, 小程序 | Y |
| 22 | 超级白板文件转换 | PPT 转码服务 | ppt转码, 文档转换 | Y |
| 23 | Express Video 服务端 | RTC 服务端 SDK | rtc-server-sdk, 服务端sdk | Y |
| 24 | Express CDN直播/LFL推流 | 旁路推流 | 旁路推流, cdn, 推流 | Y |
| 25 | Express Video 混流 | 云端转码 | 云端转码, 混流, transcode | Y |
| 26 | Express Video RTMP拉流 | RTMP 网关 | rtmp, 网关, 拉流 | Y |
| 27 | 大班课/小班课/AI大班课 | 灵动课堂（**Legacy**） | flexible-classroom, 灵动课堂 | Legacy |
| 28 | 视频会议方案 | 灵动会议 | 灵动会议, meeting | Y |
| 29 | SLA 服务可用性协议 | Status Page | status, 服务状态 | Y |
| 30 | Express Video 硬件接入 | 媒体流加速 RTSA | rtsa, 媒体流加速 | Y |

验证时间：2025-05-22，通过打开 https://doc.shengwang.cn/ 首页确认所有产品名称和分类。

---

## 关键差异总结

### 产品策略差异

| 维度 | ZEGO | Agora |
|---|---|---|
| UIKit | 独立产品（Call Kit、Live Streaming Kit 等） | 无独立 UIKit，使用低代码平台（灵动会议） |
| 教育方案 | 按场景拆分（大班课、小班课、AI大班课、美术、音乐、编程） | 灵动课堂已 Legacy，改用场景化方案（一对一、一对多、超级小班课） |
| IM | 单一 ZIM 产品 | 拆为 IM + RTM 两个产品 |
| 数字人 | 独立数字人 API | 对话式 AI 引擎（含语音对话，无独立数字人） |
| 美颜 | 独立 AI 美颜产品 | SDK 拓展插件（非独立产品） |
| 小程序 | Express Video 小程序端 | 微呼叫（独立产品） |
| PPT 转码 | 超级白板内置功能 | 独立 PPT 转码服务 |
| 状态监控 | 星图（独立产品）+ SLA 协议 | 水晶球 + Status Page（公开状态页） |
| IOT | Express Video 硬件接入（无独立品牌） | 独立 IOT 解决方案（门铃、手表、摄像头等） |
| Legacy 管理 | 无明确 Legacy 区分 | 明确标注 Legacy 产品和方案 |

---

## 查询技巧

1. **中英文关键词**：MCP 支持中英文搜索，建议两种语言都尝试
2. **产品缩写**：`rtc`, `rtm`, `rtm2` 等缩写是高效搜索词
3. **功能+平台**：如 `rtc android 集成`、`whiteboard web` 等组合查询更精确
4. **先搜索再获取内容**：先用 `search-docs` 找到文档 uri，再用 `get-doc-content` 获取完整内容
5. **ZIM 双映射**：ZEGO ZIM 需同时查 Agora IM（聊天功能）和 RTM（信令功能）
6. **Legacy 产品**：灵动课堂、语音通话、视频通话等已 Legacy，MCP 仍可搜索但文档不再更新
