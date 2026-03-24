# Links and Resources

Link syntax and local resource upload guidelines.

## Link Syntax

### Types of Links

| Type | Syntax | Example |
|------|--------|---------|
| Relative path | `[text](./path/to/file.mdx)` | `[API 文档](./api/overview.mdx)` |
| Internal link | `[text](/some/slug)` | `[快速开始](/quick-start)` |
| Anchor link | `[text](#anchor)` | `[参数说明](#parameters)` |
| External link | `[text](https://domain.com/path)` | `[GitHub](https://github.com)` |

### Best Practices for Links

1. **Use relative paths when MDX files are imported by multiple platforms** – This ensures that platform-specific documentation can automatically resolve the correct link per platform without manual updates.
2. **Use internal links (URL paths) except when relative paths are needed for multi-platform reuse** – This ensures stable navigation and reduces maintenance, unless a relative path is required for documentation reused across platforms.
3. **Use lowercase anchors** - Anchor IDs are automatically lowercased

## Local Resource Upload

### Supported Scenarios

Local file paths (not starting with `http://` or `https://`) can be uploaded to CDN via VSCode plugin upload button:

- Markdown image: `![alt](/local/path/image.png)`
- Markdown link: `[文字](/local/path/file.pdf)`
- HTML img: `<img src="/local/path/image.png" />`
- Frame component images
- Video component videos
- Button/Card icon attributes
- Any component referencing local resources

### Upload Process

1. Add local file path to MDX
2. Click the **upload button** in VSCode plugin
3. Plugin uploads files to CDN and updates paths

### File Size Guidelines

| Resource Type | Recommended Max Size |
|---------------|---------------------|
| Images | < 500KB (prefer WebP/PNG) |
| Videos | < 5MB (compress if larger) |
| PDFs | < 10MB |

### Video Compression

For videos larger than 5MB:

```bash
ffmpeg -i input.mp4 -c:v libx264 -crf 28 -preset slow -c:a copy -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" output.mp4
```

## Common Mistakes

| Mistake | Correct |
|---------|---------|
| `[text](www.zego.im/path)` | `[text](https://www.zego.im/path)` |
| `![img](C:\Users\image.png)` | `![img](./images/image.png)` |
| `[text](#Anchor Name)` | `[text](#anchor-name)` |
