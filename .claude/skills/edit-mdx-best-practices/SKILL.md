---
name: edit-mdx-best-practices
description: This skill should be used when editing MDX files, writing MDX content, adding components to documentation, or formatting documentation in ZEGO docs. Triggers on "edit mdx", "write mdx", "add callout", "create tabs", "insert steps", "mdx component", "mdx syntax", "format documentation", "编写 MDX", "编辑 MDX", "添加组件".
---

# MDX Best Practices

Guide for writing MDX documentation in ZEGO docs. Use this skill to determine the appropriate component or syntax for different content scenarios.

## Quick Decision Guide

Use this table to quickly find the right component for your content:

| Content Scenario | Recommended Component | Reference |
|------------------|----------------------|-----------|
| Warning/notice/tip messages | Use callout shortcuts (`<Note>`, `<Tip>`, `<Warning>`, `<Error>`) instead of `<Callout>` | `references/callout-components.md` |
| Multi-platform/case-specific examples | `<Tabs>` + `<Tab>` | `references/navigation-components.md` |
| Step-by-step tutorials | `<Steps>` + `<Step>` | `references/layout-components.md` |
| Collapsible detailed info | `<Accordion>` | `references/navigation-components.md` |
| Navigation cards/guides | `<CardGroup>` + `<Card>` | `references/navigation-components.md` |
| Clickable buttons/links | `<Button>` | `references/navigation-components.md` |
| Images with captions | `<Frame>` | `references/layout-components.md` |
| Video embedding | `<Video>` | `references/layout-components.md` |
| QR codes | `<QRCode>` | `references/layout-components.md` |
| API parameters/methods | `<ParamField>` | `references/api-documentation.md` |
| Multiple code samples | `<CodeGroup>` | `references/code-features.md` |
| Flowcharts/diagrams | Mermaid code block | `references/code-features.md` |
| Conditional rendering content (usually for platform differences) | `:::if{}` conditional rendering syntax | `references/conditional-rendering.md` |
| Tables with formatting | Enhanced table syntax | `references/enhanced-table-features.md` |
| Links and file uploads | Markdown links | `references/links-and-resources.md` |

## Core Workflow for Editing MDX

### 1. Identify Content Type

Before adding components, identify what the content needs:

1. **Informational** → Callout components
2. **Organizational** → Tabs, Steps, Accordion
3. **Navigational** → Card, Button
4. **Media** → Frame, Video, QRCode
5. **Technical** → ParamField, CodeGroup, Mermaid
6. **Conditional** → Platform/version-specific rendering

### 2. Choose Minimal Components

Follow the principle of minimal necessary complexity:

- Use shortcut components when available (`<Note>` over `<Callout type="note">`)
- Prefer using the `<Frame>` component for images to control their size; avoid plain Markdown images when possible.
- Combine components only when semantically appropriate

### 3. Common Patterns

**Multi-platform/case-specific documentation:**
```mdx
<Tabs>
  <Tab title="iOS">
    iOS-specific content here.
  </Tab>
  <Tab title="Android">
    Android-specific content here.
  </Tab>
</Tabs>
```

**Conditional rendering content:**

undefined means the current platform is not specified. Most of the time, it means the file is imported by other files, and it cannot set attributes for itself. So it cannot determine its own platform.

We assume the following example is written on the Android platform:
```mdx
:::if{props.platform="iOS|undefined"}
Android and iOS shared content here.
:::
:::if{props.platform="Web"}
Web-specific content here.
:::
```

**API documentation structure:**
```mdx
<ParamField
  name="methodName"
  prototype="static methodName(param: Type): ReturnType"
  desc="Brief description"
  parent_name="ClassName"
  parent_type="class"
>
  Detailed description and parameter tables.
</ParamField>
```

**Step-by-step tutorial:**
```mdx
<Steps>
  <Step title="Setup">Setup instructions</Step>
  <Step title="Configure">Configuration details</Step>
  <Step title="Run">How to run</Step>
</Steps>
```

**Table with formatting:**
```mdx
| 分类-30%-l | 数值-20%-r | 名称-50%-c |
|------------|------------|------------|
| 水果       | 100        | 橘子       |
| !mu       | 100        | 苹果       |
```

## Important Rules

### Link Syntax

Always use correct link formats:
- Relative path: `[text](./path/to/file.mdx)`
- Absolute path: `[text](/some/slug)`
- External link: `[text](https://domain.com/path)`
- Anchor: `[text](#anchor-id)`

1. **Use relative paths when MDX files are imported by multiple platforms** – This ensures that platform-specific documentation can automatically resolve the correct link per platform without manual updates.
2. **Use internal links (URL paths) except when relative paths are needed for multi-platform reuse** – This ensures stable navigation and reduces maintenance, unless a relative path is required for documentation reused across platforms.
3. **Use lowercase anchors** - Anchor IDs are automatically lowercased

### Local Resources

Local files (images, videos, PDFs) must be uploaded via VSCode plugin upload button before publishing. The system supports:
- Markdown image/link syntax
- HTML img tags
- Component attributes (icon, src, etc.)

### Code Blocks

Use appropriate language identifiers and file names:
````markdown
```javascript example.js
const code = "here";
```
````

For highlighting, use `!mark`, `!focus`, or regex patterns (see `references/code-features.md`).

## Reference Files

For detailed usage, syntax, and examples, consult these reference files:

- **`references/callout-components.md`** - Callout, Note, Tip, Warning, Error usage
- **`references/navigation-components.md`** - Tabs, Accordion, Card, Button
- **`references/layout-components.md`** - Steps, Frame, Video, QRCode
- **`references/code-features.md`** - Code blocks, CodeGroup, Mermaid, highlighting
- **`references/enhanced-table-features.md`** - Column width, alignment, cell merging
- **`references/api-documentation.md`** - ParamField component and anchor generation
- **`references/conditional-rendering.md`** - Platform and version-specific content
- **`references/links-and-resources.md`** - Links and local resource upload
