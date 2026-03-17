# FAQ（常见问题）结构标准

## 文档结构概述

**一个 FAQ 文档 = 一个问题 + 一个答案**。每个 FAQ 是独立的 `.mdx` 文件。

```
faq/
├── title.tsx              # Title 组件（目录级，无需修改）
├── ArticleMetadata.tsx    # 元数据组件（目录级，无需修改）
├── overview.mdx            # 概述页面，所有问题的列表
├── question-1.mdx         # 单个问题文档
├── question-2.mdx         # 单个问题文档
└── ...
```

## 文档模板

```mdx
---
date: "2024-01-15"
---
import { Title } from './title';
import ArticleMetadata from './ArticleMetadata';

<Title>[问题标题]？</Title>

<ArticleMetadata language="zh" product="Video Call / Audio Call / Live streaming" platform="iOS / Android / macOS / Windows" />

---

[答案内容]
```

## 必需内容

| 内容 | 要求 | 说明 |
|------|------|------|
| **date** | frontmatter 日期 | 文档创建/更新日期 |
| **Title** | 问题标题，以问号结尾 | 如：`<Title>怎么处理音频回声问题？</Title>` |
| **ArticleMetadata** | 元数据标签 | 包含 language、product、platform |
| **答案** | 问题的解答 | 直接回答，可包含章节、列表、表格 |

## ArticleMetadata 属性

| 属性 | 说明 | 示例 |
|------|------|------|
| `language` | 文档语言 | `"zh"`、`"en"` |
| `product` | 产品名称，多个用 `/` 分隔 | `"Video Call / Live streaming"`。中文写中文，英文写英文，具体参考 `overview.mdx` 里的 productData 定义|
| `platform` | 平台，多个用 `/` 分隔 | `"iOS / Android / macOS / Windows"`。中文写中文，英文写英文，具体参考 `overview.mdx` 里的 platformData 定义 |

---

## 示例

### 简单问答

```mdx
---
date: "2024-01-15"
---
import { Title } from './title';
import ArticleMetadata from './ArticleMetadata';

<Title>ZEGO Express SDK 是否支持拉 60 帧的流？</Title>

<ArticleMetadata language="zh" product="实时音视频 / 超低延迟直播" platform="iOS" />

---

支持，当推流端推流帧率大于 30 帧时，如果 iOS 端也要拉到超过 30 帧的流，请联系技术支持。其他端没有此限制，低于 60 帧无需做特殊处理。
```

### 复杂问题排查

```mdx
---
date: "2024-01-15"
---
import { Title } from './title';
import ArticleMetadata from './ArticleMetadata';

<Title>怎么处理音频回声问题？</Title>

<ArticleMetadata language="zh" product="实时音视频 / 实时语音 / 超低延迟直播" platform="iOS / Android / macOS / Windows" />

---

ZEGO SDK 提供了能够适用于绝大多数场景和设备的回声消除功能。如果存在回声问题，您可以参考如下操作步骤进行处理。

## 问题排查

<Warning title="注意">
当某个用户听到回声时，往往不是自己的问题，而是通话的对方回声消除功能失效。
</Warning>

- 如果使用了设备本身提供的回声消除功能，但是效果不佳，可以与 ZEGO 技术支持联系。
- 在使用 ZEGO SDK 提供的回声消除功能时，由于 CPU 负载过高，可能会造成回声问题：
  1. CPU 是否负载过高或者瞬时过高。
  2. 是否使用了音频前处理或者音频后处理功能。

## 联系 ZEGO 技术支持

如果问题仍然存在，请联系 ZEGO 技术支持，并提供以下信息：

| 信息 | 详情 |
|------|------|
| 必要信息 | roomID、userID |
| 可选信息 | 出现问题的时间段、SDK 日志 |
```

---

## 写作规范

### 问题标题

1. **用户视角提问** - 使用用户会问的真实问题
2. **问号结尾** - 标题以 `？`（中文）或 `?`（英文）结尾
3. **简洁明确** - 一眼能看出问题内容

**好的标题：**
- `怎么处理音频回声问题？`
- `ZEGO Express SDK 是否支持拉 60 帧的流？`

**不好的标题：**
- `音频回声` （不是问题形式）
- `关于回声问题的说明` （太笼统）

### 答案内容

1. **先给结论** - 开篇直接回答问题
2. **再给步骤** - 需要操作步骤时使用有序列表
3. **注意事项** - 使用 `<Warning>` 组件突出显示

---

## 检查清单

- [ ] frontmatter 包含 date
- [ ] Title 组件存在且以问号结尾
- [ ] ArticleMetadata 属性正确（language、product、platform）
- [ ] 答案内容直接回答问题
- [ ] Warning 组件用于注意事项
- [ ] 复杂问题包含联系技术支持信息
