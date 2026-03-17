# Navigation Components

Components for organizing and navigating content.

## Tabs / Tab

Organize content into switchable tabs. Perfect for multi-platform documentation.

### Tabs Attributes

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| titleSize | `"p" \| "h2" \| "h3" \| "h4" \| "h5"` | `"p"` | Title level for TOC |

### Tab Attributes

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| title | `string` | Yes | Tab title |
| titleSize | `"p" \| "h2" \| "h3" \| "h4" \| "h5"` | No | Override parent titleSize |

**Example:**
```mdx
<Tabs>
  <Tab title="iOS">
    iOS 平台的实现代码
  </Tab>
  <Tab title="Android">
    Android 平台的实现代码
  </Tab>
  <Tab title="Web">
    Web 平台的实现代码
  </Tab>
</Tabs>
```

## Accordion

Collapsible content panels for optional or detailed information.

### Attributes

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| title | `string` | - | Panel title |
| defaultOpen | `"true" \| "false"` | `"false"` | Whether expanded by default |

**Example:**
```mdx
<Accordion title="点击展开详情" defaultOpen="false">
  这里是折叠的详细内容。
</Accordion>
```

## Card / CardGroup

Card-style layout for navigation guides and feature highlights.

### CardGroup Attributes

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| cols | `number` | `2` | Number of columns (1-5) |

### Card Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| title | `string` | Card title |
| icon | `string \| ReactNode` | Icon (URL or component) |
| href | `string` | Click navigation link |
| target | `string` | Link target |

**Example:**
```mdx
<CardGroup cols={3}>
  <Card title="快速开始" icon="/icons/start.svg" href="/quick-start">
    5 分钟快速接入 SDK
  </Card>
  <Card title="API 文档" icon="/icons/api.svg" href="/api-reference">
    查看完整 API 参考
  </Card>
  <Card title="示例代码" icon="/icons/code.svg" href="/samples">
    下载示例项目
  </Card>
</CardGroup>
```

## Button

Clickable buttons for calls-to-action.

### Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| href | `string` | Navigation link |
| target | `"_self" \| "_blank"` | Link target |
| primary-color | `string` | Theme color |
| icon | `string \| ReactNode` | Button icon |
| circular | `boolean` | Circular button style |
| tip | `string` | Hover tooltip |

### Available Colors

`DarkGray` `NavyBlue` `Orange` `Tangerine` `Red` `Magenta` `Purple` `LightBlue` `Turquoise` `Green` `Lime` `Gray` `White`

**Example:**
```mdx
<Button href="https://github.com/example" target="_blank" primary-color="NavyBlue">
  下载示例
</Button>
```

## When to Use Each

| Scenario | Component |
|----------|-----------|
| Platform/version switching | `<Tabs>` |
| Optional detailed content | `<Accordion>` |
| Landing page navigation | `<CardGroup>` + `<Card>` |
| Call-to-action buttons | `<Button>` |
