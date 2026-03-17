# docuo.config.json 配置说明

本文档介绍 `docuo.config.json` 配置文件的完整语法规则。

---

## 文件结构概览

```json
{
  "title": "站点标题",
  "favicon": "image/favicon.ico",
  "themeConfig": { ... },
  "instances": [ ... ],
  "analytics": { ... },
  "i18n": { ... },
  "sitemap": { ... },
  "redirects": [ ... ],
  "passthroughPrefixes": [ ... ]
}
```

---

## 基础配置

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `title` | `string` | 是 | 站点标题 |
| `description` | `string` | 否 | 站点描述 |
| `favicon` | `string` | 是 | 网站图标路径 |
| `url` | `string` | 否 | 站点 URL |
| `passthroughPrefixes` | `string[]` | 否 | 不做路径转换的前缀列表 |

---

## themeConfig - 主题配置

### 颜色配置

```json
{
  "themeConfig": {
    "colors": {
      "primaryLight": "#0055FF",
      "primaryDark": "#266EFF"
    },
    "colorMode": {
      "defaultMode": "light",
      "disableSwitch": false,
      "respectPrefersColorScheme": false
    },
    "removeWatermark": true,
    "showAskAI": true
  }
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `colors.primaryLight` | `string` | 浅色模式主色 |
| `colors.primaryDark` | `string` | 深色模式主色 |
| `colorMode.defaultMode` | `"light" \| "dark" \| "system"` | 默认颜色模式 |
| `colorMode.disableSwitch` | `boolean` | 禁用模式切换 |
| `removeWatermark` | `boolean` | 移除水印 |
| `showAskAI` | `boolean` | 显示 AI 问答入口 |

### 导航栏配置 (navbar)

支持多语言，使用后缀区分：`navbar`（默认）、`navbar.zh`（中文）

```json
{
  "themeConfig": {
    "navbar": {
      "title": "站点名称",
      "logo": {
        "dark": "image/logo_dark.png",
        "light": "image/logo_light.png"
      },
      "iconRedirectUrl": "https://example.com",
      "items": [
        { "type": "default", "label": "控制台", "href": "https://console.example.com" },
        { "type": "button", "label": "登录", "href": "https://login.example.com" }
      ]
    }
  }
}
```

**导航项类型 (items.type)：**
| 类型 | 说明 |
|------|------|
| `default` | 普通链接 |
| `button` | 按钮样式 |
| `docSidebar` | 文档侧边栏链接 |
| `dropdown` | 下拉菜单 |
| `docsVersionDropdown` | 版本下拉 |
| `docsInstanceDropdown` | 实例下拉 |
| `search` | 搜索框 |

### 页脚配置 (footer)

```json
{
  "themeConfig": {
    "footer": {
      "logo": { "dark": "...", "light": "..." },
      "caption": "地址信息",
      "copyright": { "label": "版权信息", "href": "https://..." },
      "links": [
        {
          "title": "开发者中心",
          "items": [
            { "label": "SDK 中心", "href": "https://..." }
          ]
        }
      ],
      "socials": [
        { "logo": "GitHub", "href": "https://github.com/..." }
      ],
      "policies": [
        { "label": "隐私政策", "href": "https://..." }
      ]
    }
  }
}
```

### 实例分组 (instanceGroups)

用于组织多平台、多产品的文档导航。这个很重要。：

```json
{
  "themeConfig": {
    "instanceGroups": [
      {
        "id": "real_time_video_zh",
        "name": "实时音视频",
        "tag": "热门",
        "category": ["产品", "互动核心产品"],
        "instances": [
          {
            "id": "real_time_video_ios_oc_zh",
            "platform": "iOS: Objective-C",
            "tab": {
              "mySidebar": "文档",
              "clientApi": "客户端 API"
            }
          }
        ]
      }
    ]
  }
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | `string` | 分组唯一标识 |
| `name` | `string` | 分组显示名称 |
| `tag` | `string` | 标签（如"热门"、"新"） |
| `category` | `string[]` | 分类层级 |
| `instances` | `array` | 包含的实例列表 |
| `instances[].id` | `string` | 实例 ID（对应 instances 配置） |
| `instances[].platform` | `string` | 平台显示名称 |
| `instances[].tab` | `string \| object` | Tab 配置 |

**Tab 配置格式：**
- 字符串：`"文档"` 等价于 `{ "mySidebar": "文档" }`
- 对象：`{ "sidebarId": "Tab名称","clientApi": "客户端 API" , "https://...": "外链名称" }`

---

## instances - 文档实例配置

每个实例代表一个独立的文档集合，拥有自己的路由、侧边栏和版本。这个也很重要：

```json
{
  "instances": [
    {
      "id": "real_time_video_ios_oc_zh",
      "label": "实时音视频",
      "path": "core_products/real-time-voice-video/zh/ios-oc",
      "clientApiPath": "client-sdk/api-reference",
      "routeBasePath": "real-time-video-ios-oc",
      "locale": "zh"
    }
  ]
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `id` | `string` | 是 | 实例唯一标识，需与 instanceGroups 中引用一致 |
| `label` | `string` | 否 | 实例显示名称 |
| `path` | `string` | 是 | 文档目录相对路径（相对于 docs 目录） |
| `clientApiPath` | `string` | 否 | 客户端 API 文档路径 |
| `routeBasePath` | `string` | 是 | URL 路由前缀 |
| `locale` | `string` | 否 | 语言标识（如 "zh"、"en"） |
| `versions` | `array` | 否 | 版本配置列表 |
| `versions[].version` | `string` | 是 | 版本号 |
| `versions[].path` | `string` | 是 | 版本目录路径 |

---

## sidebars.json - 侧边栏配置

每个实例目录下可包含 `sidebars.json` 文件，定义该实例的侧边栏结构。

### 文档 ID 概念

**文档 ID** 是侧边栏中引用文档的核心标识，规则如下：

1. **相对路径**：ID 是相对于实例目录的文件路径，**不包含文件扩展名**
2. **路径分隔符**：使用 `/` 分隔目录层级

### 文档 ID 转换规则


```typescript
// 转换规则：
// 1. 大写字母 → 小写字母
// 2. 空格 → 连字符 (-)
// 3. URL编码空格 (%20) → 连字符 (-)
// 4. Windows反斜杠 (\) → 正斜杠 (/)
```

**转换示例**：

| 原始路径/ID | 转换后的文档 ID |
|------------|----------------|
| `Quick Start` | `quick-start` |
| `Quick-Start` | `quick-start` |
| `Introduction/Overview` | `introduction/overview` |
| `API Reference/Class` | `api-reference/class` |
| `01-Getting Started` | `getting-started`（数字前缀被移除） |

### 数字前缀处理

文件/目录名中的数字前缀（如 `01-`、`02-`）会被自动移除，用于控制排序但不影响最终 ID：

| 文件名 | 文档 ID |
|--------|---------|
| `01-introduction.mdx` | `introduction` |
| `02-quick-start/01-setup.mdx` | `quick-start/setup` |

正则规则：`/^(\d+)-/`（匹配开头的 `数字-` 格式）

### 示例

假设实例目录为 `docs/core_products/real-time-voice-video/zh/ios-oc/`

| 文件路径 | 文档 ID |
|---------|---------|
| `introduction/overview.mdx` | `introduction/overview` |
| `01-Introduction/02-Overview.mdx` | `introduction/overview` |
| `Quick Start/Setup Guide.mdx` | `quick-start/setup-guide` |
| `client-sdk/API Reference/Class.mdx` | `client-sdk/api-reference/class` |

### URL 映射

文档 ID 会与实例的 `routeBasePath` 组合生成最终 URL：
- 实例 `routeBasePath`: `real-time-video-ios-oc`
- 文档 ID: `introduction/overview`
- 最终 URL: `/real-time-video-ios-oc/introduction/overview`

### 基本结构

```json
{
  "mySidebar": [ ... ],
  "clientApi": [ ... ]
}
```

键名对应 Tab 配置中的 sidebarId。

### 侧边栏项类型

#### 1. doc - 文档链接

```json
{
  "type": "doc",
  "label": "概述",
  "id": "introduction/overview",
  "articleID": 5413,
  "visible": true
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `type` | `"doc"` | 类型标识 |
| `label` | `string` | 显示名称 |
| `id` | `string` | 文档 ID（相对于实例目录的路径，不含扩展名） |
| `articleID` | `number` | 文章 ID（可选，用于追踪） |
| `visible` | `boolean` | 是否在侧边栏显示（默认 true） |

#### 2. category - 分类目录

```json
{
  "type": "category",
  "label": "产品简介",
  "collapsed": false,
  "collapsible": true,
  "items": [
    { "type": "doc", "label": "概述", "id": "introduction/overview" },
    { "type": "doc", "label": "功能列表", "id": "introduction/features" }
  ]
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `type` | `"category"` | 类型标识 |
| `label` | `string` | 分类名称 |
| `collapsed` | `boolean` | 是否默认折叠 |
| `collapsible` | `boolean` | 是否可折叠 |
| `visible` | `boolean` | 是否显示 |
| `items` | `array` | 子项列表 |
| `tag` | `object` | 标签配置 `{ "label": "新", "color": "#ff0000" }` |

#### 3. link - 外部链接

```json
{
  "type": "link",
  "label": "GitHub",
  "href": "https://github.com/example"
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `type` | `"link"` | 类型标识 |
| `label` | `string` | 链接文本 |
| `href` | `string` | 链接地址（支持绝对路径和相对路径） |

#### 4. autogenerated - 自动生成

```json
{
  "type": "autogenerated",
  "dirName": "guides"
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `type` | `"autogenerated"` | 类型标识 |
| `dirName` | `string` | 目录名（"." 表示当前目录） |

### 简写语法

可以直接使用字符串表示文档 ID：

```json
{
  "mySidebar": [
    "introduction/overview",
    "introduction/features",
    {
      "type": "category",
      "label": "指南",
      "items": ["guides/quick-start", "guides/advanced"]
    }
  ]
}
```

---

## analytics - 统计分析

```json
{
  "analytics": {
    "ga4": { "measurementId": "G-XXXXXXXXXX" },
    "baidu": { "tongjiID": "xxxxxxxxxxxxxxxx" }
  }
}
```

---

## i18n - 国际化

```json
{
  "i18n": {
    "defaultLocale": "zh",
    "localeConfigs": {
      "zh": "中文",
      "en": "English"
    }
  }
}
```

---

## sitemap - 站点地图

```json
{
  "sitemap": {
    "siteUrl": "https://doc-zh.zego.im"
  }
}
```

---

## redirects - 重定向规则

```json
{
  "redirects": [
    {
      "source": "/old-path/:path*",
      "destination": "/new-path/:path*"
    },
    {
      "source": "/legacy-doc",
      "destination": "/new-doc"
    }
  ]
}
```

支持动态路径参数：`:path*` 匹配任意路径，`:platform` 匹配单个路径段。

