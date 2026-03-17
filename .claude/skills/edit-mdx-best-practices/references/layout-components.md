# Layout Components

Components for content layout and media display.

## Steps / Step

Display ordered step-by-step procedures.

### Steps Attributes

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| titleSize | `"p" \| "h2" \| "h3" \| "h4" \| "h5"` | `"p"` | Step title level |

### Step Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| title | `string` | Step title |
| icon | `string \| ReactNode` | Custom icon |
| stepNumber | `number` | Custom step number |

**Example:**
```mdx
<Steps>
  <Step title="创建项目">
    使用 Xcode 创建一个新的 iOS 项目。
  </Step>
  <Step title="添加依赖">
    通过 CocoaPods 添加 ZEGO SDK。
  </Step>
  <Step title="初始化 SDK">
    在 AppDelegate 中初始化 SDK。
  </Step>
</Steps>
```

## Frame

Image container with caption and zoom support.

### Attributes

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| width | `string` | `"auto"` | Width (px or %) |
| height | `string` | `"auto"` | Height (px or %) |
| caption | `string` | - | Image caption |

**Example:**
```mdx
<Frame width="400" caption="架构示意图">
  <img src="/images/architecture.png" alt="架构图" />
</Frame>
```
**注意**：不要使用 `![]()` 语法，而是使用 `<img />` 标签，并且添加 `alt` 属性。

## Video

Embed videos from YouTube, Vimeo, Loom, or local files.

### Attributes

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| src | `string` | - | Video URL (required) |
| width | `string` | `"100%"` | Width |
| height | `string` | `"auto"` | Height |

**Examples:**
```mdx
<!-- YouTube (auto-converts to embed) -->
<Video src="https://www.youtube.com/watch?v=xxxxx" />

<!-- Vimeo -->
<Video src="https://vimeo.com/123456789" />

<!-- Local video -->
<Video src="/videos/demo.mp4" width="640" height="360" />
```

### Video Compression

For videos larger than 5MB, compress before uploading:

```bash
ffmpeg -i input.mp4 -c:v libx264 -crf 28 -preset slow -c:a copy -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" output.mp4
```

## QRCode

Generate QR codes dynamically.

### Attributes

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| content | `string` | - | QR code content (required) |
| size | `number` | `200` | Size in pixels |
| errorCorrectionLevel | `"L" \| "M" \| "Q" \| "H"` | `"M"` | Error correction level |
| title | `string` | - | QR code title |
| showTitle | `boolean` | `false` | Show title |

**Example:**
```mdx
<QRCode content="https://www.zego.im" size={150} showTitle={true} title="扫码访问官网" />
```

## When to Use Each

| Scenario | Component |
|----------|-----------|
| Tutorial procedures | `<Steps>` |
| Image with caption | `<Frame>` |
| Video content | `<Video>` |
| Mobile app links | `<QRCode>` |
