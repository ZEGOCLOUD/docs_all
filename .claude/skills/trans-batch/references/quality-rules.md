# 翻译质量规则

## 核心原则

- ✅ **必须使用术语对照表**：每次翻译前都要重新加载，不能依赖记忆或缓存
- ✅ **忠于原文**：禁止随意扩写或捏造内容
- ✅ **手动翻译**：禁止使用自动化翻译工具或第三方翻译 API
- ✅ **准确性优先**：翻译质量比速度更重要

---

## 标点符号处理

### 中文标点转为英文标点

- `。` → `.`（句号）
- `，` → `,`（逗号）
- `；` → `;`（分号）
- `：` → `:`（冒号）
- `（）` → `()`（括号）
- `《》` → `""` 或斜体（书名号）

### 示例

**原文**：
```
这是一个测试，请注意标点符号。
```

**翻译**：
```
This is a test, please pay attention to punctuation.
```

---

## YAML 特殊规则

### 中文冒号处理

**规则**：如果 YAML 描述是单行且包含中文冒号 `：`，必须改为多行描述（使用 `|`）

**错误示例**：
```yaml
description: 接口名称：获取用户列表
```

**正确示例**：
```yaml
description: |
  Interface name: Get user list
```

**原因**：YAML 解析器可能将冒号误认为字段分隔符

---

## 转义字符处理

### MDX/JSX 特殊字符

**规则**：
- ✅ 保留原有的反斜杠转义符，不要删除
- ✅ 翻译后如果造成 JSX/MDX 语法错误，**必须添加转义符**

**需要转义的字符**：
- `<` → `\<`
- `>` → `\>`
- `{` → `\{`
- `}` → `\}`
- `:` → `\:` （在特定位置，如 JSX 属性值中）

### 示例

**原文**：
```markdown
请使用 <Button> 组件
```

**错误翻译**：
```markdown
Please use <Button> component
```

**正确翻译**：
```markdown
Please use \<Button\> component
```

---

## 内容准确性

### 链接和引用

- ✅ **链接地址**：可以按中英文实际情况调整
- ✅ **内部链接名称**：优先使用 `sidebars.json` 中定义的 label
- ✅ **翻译结果不能出现中文和中文标点符号**，杜绝中英混杂

### 示例

**原文**：
```markdown
参见 [快速开始](./quick-start.md) 了解更多信息。
```

**翻译**：
```markdown
See [Quick Start](./quick-start.md) for more information.
```

---

## 内容保持不变

### 代码块

**规则**：代码保持原样不翻译，注释要翻译

**示例**：

```javascript
// 创建一个新用户
const user = createUser();  // 这行注释需要翻译
```

**翻译**：
```javascript
// Create a new user
const user = createUser();
```

### URL 和 API 端点

**规则**：保持原样（翻译对照表中明确说明的除外）

**示例**：
- `https://example.com/api/users` → 不变
- `GET /api/v1/users` → 不变
- `https://console.zego.im` → `https://console.zegocloud.com`（对照表有说明）

### 技术标识符

**规则**：保持原样

**示例**：
- `ZegoExpressEngine` → 不变
- `RoomID` → 不变
- `useState` → 不变

### 参数名和字段名

**规则**：保持原样

**示例**：
```yaml
parameters:
  - name: room_id
    description: 房间 ID
```

**翻译**：
```yaml
parameters:
  - name: room_id
    description: Room ID
```

### Frontmatter

**规则**：翻译值但保持键名不变

**示例**：
```yaml
---
title: 快速开始
description: 本文档介绍如何快速开始使用 ZEGO
---
```

**翻译**：
```yaml
---
title: Quick Start
description: This document introduces how to quickly get started with ZEGO
---
```

---

## 格式保持

### Markdown 语法

**规则**：保留所有 markdown 语法

**示例**：
```markdown
# 标题
**粗体**
*斜体*
[链接](url)
`代码`
```

**翻译**：保留所有格式标记

### 表格结构

**规则**：保留表格结构，翻译单元格内容

**示例**：

**原文**：
```markdown
| 参数 | 类型 | 说明 |
|------|------|------|
| roomID | String | 房间 ID |
```

**翻译**：
```markdown
| Parameter | Type | Description |
|-----------|------|-------------|
| roomID | String | Room ID |
```

### 列表格式

**规则**：保留列表格式（有序列表、无序列表）

### YAML 结构和缩进

**规则**：保留 YAML 结构和缩进，只翻译描述性字段的值

---

## 常见错误

### 错误 1：中英混杂

❌ **错误**：
```
This is a 测试 file。
```

✅ **正确**：
```
This is a test file.
```

### 错误 2：保留中文标点

❌ **错误**：
```
This is a test，please note.
```

✅ **正确**：
```
This is a test, please note.
```

### 错误 3：随意扩写

❌ **错误**：
```
**原文**：点击按钮
**翻译**：Please click on the button that is located at the bottom right corner of the screen
```

✅ **正确**：
```
**原文**：点击按钮
**翻译**：Click the button
```

### 错误 4：翻译代码

❌ **错误**：
```javascript
const 用户 = createUser();  // 翻译了变量名
```

✅ **正确**：
```javascript
const user = createUser();  // 变量名保持不变
```

---

## 术语一致性

### 通用术语

从 `.translate/common-terminology.csv` 加载

**常见术语**：
```
ZEGO → ZEGOCLOUD
ZEGO 控制台 → ZEGOCLOUD Console
实时音视频 → Real-Time Audio and Video
超低延迟直播 → Ultra-Low Latency Live Streaming
```

### 产品特定术语

从 `.translate/products/<产品ID>.csv` 加载

**RTC 产品术语**：
```
推流 → Publish stream
拉流 → Play stream
房间 → Room
用户 → User
```

---

## 质量检查清单

翻译完成后，检查以下项目：

- [ ] 所有中文标点符号已转为英文标点
- [ ] 没有中文和中文标点符号残留
- [ ] 代码块保持原样
- [ ] URL 和 API 端点保持原样
- [ ] 技术标识符保持原样
- [ ] 参数名和字段名保持原样
- [ ] Markdown 格式保持完整
- [ ] 表格结构正确
- [ ] 术语与术语表一致
- [ ] 没有 JSX/MDX 语法错误（如有需要已添加转义符）
- [ ] YAML 描述如包含冒号已改为多行
- [ ] Frontmatter 键名保持不变，值已翻译
- [ ] 没有随意扩写或捏造内容
