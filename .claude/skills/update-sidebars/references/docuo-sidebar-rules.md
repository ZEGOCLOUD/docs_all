# DOCUO Sidebar Configuration Reference

Quick reference for understanding DOCUO sidebar configuration and document ID rules.

## Document ID Rules

Document IDs are the primary way to reference documents in sidebar configuration. They follow these conversion rules:

### Conversion Rules

1. **Relative path**: ID is relative to the instance directory, without file extension
2. **Path separator**: Uses `/` (forward slash)
3. **Lowercase**: All letters converted to lowercase
4. **Spaces to hyphens**: Spaces become `-`
5. **Number prefixes**: Files/directories with `01-`, `02-` prefixes have them removed

### Examples

| File Path | Document ID |
|-----------|-------------|
| `introduction/overview.mdx` | `introduction/overview` |
| `01-Introduction/02-Overview.mdx` | `introduction/overview` |
| `Quick Start/Setup Guide.mdx` | `quick-start/setup-guide` |
| `client-sdk/API Reference/Class.mdx` | `client-sdk/api-reference/class` |

### URL Generation

Document IDs combine with `routeBasePath` to form final URLs:

- Instance `routeBasePath`: `real-time-video-android-java`
- Document ID: `introduction/overview`
- Final URL: `/real-time-video-android-java/introduction/overview`

## Sidebar Item Types

### 1. doc - Document Link

```json
{
  "type": "doc",
  "label": "Overview",
  "id": "introduction/overview",
  "articleID": 5413,
  "visible": true
}
```

**Fields:**
- `type`: "doc" (required)
- `id`: Document ID (required)
- `label`: Display text (what this skill updates)
- `articleID`: Article tracking number (optional)
- `visible`: Show in sidebar (optional, default: true)

### 2. category - Category

```json
{
  "type": "category",
  "label": "Getting Started",
  "collapsed": false,
  "collapsible": true,
  "items": [...]
}
```

### 3. link - External Link

```json
{
  "type": "link",
  "label": "GitHub",
  "href": "https://github.com/example"
}
```

## Sidebars File Location

Each instance has its own `sidebars.json` in the instance directory:

```
docs/
└── core_products/
    └── real-time-voice-video/
        └── en/
            └── android-java/
                ├── sidebars.json          ← Sidebar configuration
                ├── introduction/
                │   └── overview.mdx
                └── quick-start/
                    └── setup.mdx
```

## Instance Path Mapping

From `docuo.config.json`:

```json
{
  "instances": [
    {
      "id": "real_time_video_android_java_en",
      "path": "core_products/real-time-voice-video/en/android-java",
      "routeBasePath": "real-time-video-android-java",
      "locale": "en"
    }
  ]
}
```

The `path` field indicates where to find both:
1. The `sidebars.json` file
2. The MDX documents referenced by document IDs

## H1 Heading Extraction

This skill extracts the first H1 heading (`# Title`) from MDX files, skipping frontmatter:

```markdown
---
articleID: 5416
date: "2023-09-04"
---
# This becomes the label

Content here...
```

Files without H1 headings are skipped and their labels remain unchanged.
