# 浏览器自动化读取腾讯云文档

使用 Playwright 或 Chrome DevTools 读取腾讯云产品文档。

---

## 为什么用浏览器自动化而不是 Web Reader

Web Reader 会剥离所有 href 链接，无法提取子文档的 URL。浏览器自动化可以：
- 获取完整页面快照（含链接和层级结构）
- 点击左侧目录导航到子文档
- 提取表格、代码块等结构化内容
- 截图辅助理解页面布局

---

## 推荐工具：Playwright

环境已配置 Playwright MCP 工具，优先使用。

### 步骤 1：打开产品总览页

```
工具: mcp__plugin_playwright_playwright__browser_navigate
参数: url = "https://cloud.tencent.com/document/product/{产品ID}"
```

### 步骤 2：获取页面快照（含目录结构）

```
工具: mcp__plugin_playwright_playwright__browser_snapshot
```

快照返回无障碍树，包含：
- 左侧目录的完整结构（章节 → 子章节 → 文档标题）
- 每个可点击元素的引用（用于后续点击导航）
- 当前页面的正文内容

### 步骤 3：点击目标章节

```
工具: mcp__plugin_playwright_playwright__browser_click
参数: target = "{目录项的引用}"
```

点击后页面自动导航到子文档。

### 步骤 4：提取子文档内容

```
工具: mcp__plugin_playwright_playwright__browser_snapshot
```

---

## 备选工具：Chrome DevTools

如果 Playwright 不可用，可使用 Chrome DevTools：

```
导航: mcp__chrome-devtools__navigate_page → url
快照: mcp__chrome-devtools__take_snapshot
点击: mcp__chrome-devtools__click → uid
```

---

## 产品总览页一览

| 产品 | 产品 ID | 总览页 URL |
|---|---|---|
| TRTC 实时音视频 | 647 | https://cloud.tencent.com/document/product/647 |
| IM 即时通信 | 269 | https://cloud.tencent.com/document/product/269 |
| CSS 云直播 | 267 | https://cloud.tencent.com/document/product/267 |
| 腾讯特效 SDK | 616 | https://cloud.tencent.com/document/product/616 |
| TIW 互动白板 | 1137 | https://cloud.tencent.com/document/product/1137 |
| 智能数智人 | 1240 | https://cloud.tencent.com/document/product/1240 |
