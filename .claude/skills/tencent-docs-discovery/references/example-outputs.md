# 示例输出格式

## 场景一：查询 TRTC 功能

**输入**：`TRTC 的混流功能有哪些`

**操作**：浏览器自动化打开 647 总览页 → 快照提取目录 → 点击「云端混流转码」章节

**输出**：

```markdown
## TRTC 混流功能

- 产品：TRTC 实时音视频（647）
- 查询方式：浏览器自动化
- 功能概述：支持云端混流转码，可将多路音视频流混合为一路

### 核心能力
- 支持 16 路流混流
- 多种布局模板（悬浮、九宫格、屏幕分享等）
- 实时切换布局
- 自定义背景图和水印

### 相关文档
- 云端混流转码接入指南
- 混流 REST API 接口说明
- 混流布局模板说明
```

---

## 场景二：查询 TUICallKit 集成

**输入**：`TUICallKit 怎么在 Web 端集成`

**操作**：浏览器自动化打开 647 总览页 → 快照提取目录 → 点击 TUICallKit 相关章节

**输出**：

```markdown
## TUICallKit Web 集成

- 对应 ZEGO 产品：Call Kit
- 支持框架：Vue 3、React

### 集成步骤
1. npm install @tencentcloud/call-uikit-vue3（Vue）/ @tencentcloud/call-uikit-react（React）
2. 初始化 TUICallKit
3. 配置 SDKAppID 和 UserSig
4. 调用 call() 或 groupCall() 发起通话
```

---

## 场景三：查询 CSS 云直播

**输入**：`腾讯云直播的 CDN 推流怎么配置`

**操作**：浏览器自动化打开 267 总览页 → 快照提取目录 → 点击 CDN 推流相关章节

**输出**：

```markdown
## CSS 云直播 CDN 推流配置

- 产品：CSS 云直播（267）
- 查询方式：浏览器自动化

### 配置步骤
1. 添加推流域名（自有域名 CNAME 到腾讯云）
2. 配置推流和播放域名
3. 生成推流 URL
4. 使用推流工具/OBS 推流

### 相关 API
- CreateLiveDomain（添加域名）
- CreateLiveStream（创建流）
```

---

## 场景四：列出所有竞品

**输入**：`列出所有腾讯云竞品及其文档访问方式`

**输出**：

```markdown
## 腾讯云竞品文档访问方式一览

所有产品统一使用浏览器自动化（Playwright）读取文档。

| ZEGO 产品 | 腾讯云产品 | 产品 ID | 总览页 URL |
|---|---|---|---|
| Express Video/Audio | TRTC 实时音视频 | 647 | https://cloud.tencent.com/document/product/647 |
| ZIM | IM 即时通信 | 269 | https://cloud.tencent.com/document/product/269 |
| LFL | CSS 云直播 | 267 | https://cloud.tencent.com/document/product/267 |
| Cloud Recording | TRTC 云端录制 | 647 | https://cloud.tencent.com/document/product/647 |
| Call Kit | TUICallKit | 647 | https://cloud.tencent.com/document/product/647 |
| Live Streaming Kit | TUILiveKit | 647 | https://cloud.tencent.com/document/product/647 |
| Live Audio Room Kit | TUILiveKit | 647 | https://cloud.tencent.com/document/product/647 |
| Video Conference Kit | TUIRoomKit | 647 | https://cloud.tencent.com/document/product/647 |
| IMKit | TUIKit | 269 | https://cloud.tencent.com/document/product/269 |
| AI Effects | 腾讯特效 SDK | 616 | https://cloud.tencent.com/document/product/616 |
| Super Board | TIW 互动白板 | 1137 | https://cloud.tencent.com/document/product/1137 |
| Digital Human | 智能数智人 | 1240 | https://cloud.tencent.com/document/product/1240 |
```
