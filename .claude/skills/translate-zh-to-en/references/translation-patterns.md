# Translation Patterns and Edge Cases

## Common Terminology Reference

### Brand Names
| Chinese | English |
|---------|---------|
| ZEGO | ZEGOCLOUD |
| ZEGO 控制台 | ZEGOCLOUD Console |
| ZEGO 技术支持 | ZEGOCLOUD Technical Support |
| 星图 | Analytics Dashboard |

### Core Products
| Chinese | English |
|---------|---------|
| 实时音视频 | Video Call |
| 实时语音 | Voice Call |
| 超低延迟直播 | Live Streaming |
| 即时通讯 | In-app Chat |
| 云端录制 | Cloud Recording |
| AI 美颜 | AI-Effects |
| 超级白板 | Super Board |
| 实时互动 AI Agent | Conversational AI |
| 数字人 API | Digital Human AI |

### UIKit Products
| Chinese | English |
|---------|---------|
| 音视频通话 UIKit | Call Kit |
| 互动直播 UIKit | Live Streaming Kit |
| 语聊房 UIKit | Live Audio Room Kit |
| IMKit | In-app Chat Kit |

### Technical Terms
| Chinese | English |
|---------|---------|
| 拉流 | Play stream |
| 推流 | Publish stream |

## Edge Cases

### MDX Component Handling

**Correct**: Translate only the attribute values
```mdx
// Before
<Card title="开始使用" description="快速集成 SDK" />

// After
<Card title="Getting Started" description="Quick SDK Integration" />
```

**Incorrect**: Do NOT translate component names or attribute keys
```mdx
// WRONG
<卡片 标题="Getting Started" 描述="Quick SDK Integration" />
```

### MDX import translation

1. Check if the snippet file for english exists, if not, create it by copying the snippet file for chinese and translate the chinese text to english text.
2. Translate the import path, change the zh to en.
```mdx
// Before
import ContentA from '/core_products/aiagent/zh/server/some-snippet.mdx'
import ContentB from '/snippets/Reuse/SignatureVerificationZH.mdx'

// After
import ContentA from '/core_products/aiagent/en/server/some-snippet.mdx'
import ContentB from '/snippets/Reuse/SignatureVerificationEN.mdx'
```

### Code Block Translation

**Translate comments only**:
```javascript
// Before
// 初始化 ZEGO Express Engine
const engine = new ZegoExpressEngine(appID, appSign);

// After
// Initialize ZEGO Express Engine
const engine = new ZegoExpressEngine(appID, appSign);
```

### YAML Frontmatter

**Translate values, keep keys**:
```yaml
# Before
---
title: 快速开始
sidebar_label: 集成指南
---

# After
---
title: Quick Start
sidebar_label: Integration Guide
---
```

### Link Text Translation

**Translate link text, keep URL unchanged**:
```markdown
// Before
[查看详细文档](/feature/guide)

// After
[View detailed documentation](/feature/guide)
```

### Table Translation

**Translate cell contents only**:
```markdown
// Before
| 参数 | 类型 | 描述 |
|------|------|------|
| appID | number | 应用 ID |

// After
| Parameter | Type | Description |
|-----------|------|-------------|
| appID | number | Application ID |
```

### Escaping Special Characters

In MDX, escape these characters when they appear in content:
- `<` → `\<`
- `>` → `\>`
- `{` → `\{`
- `}` → `\}`

Example:
```mdx
// Before (Chinese)
如果 age < 18，则返回 {error}

// After (English with escaping)
If age \< 18, return \{error\}
```

### OpenAPI YAML Translation Rules

#### Chinese Colon Handling (CRITICAL)

**Rule**: If a YAML value contains Chinese colon `：`, MUST convert to multi-line format using `|`

**Incorrect** (YAML parser will fail):
```yaml
description: 接口名称：获取用户列表
```

**Correct**:
```yaml
description: |
  Interface name: Get user list
```

**Reason**: YAML parser treats `:` after space as key-value separator, causing parsing errors.

#### Fields to Translate

Translate only description-related field values:
- `description` - descriptions
- `summary` - summaries
- `example` - example values (if they contain Chinese text)
- `title` - titles
- `x-extensions` - custom extension descriptions

#### Fields to Keep Unchanged

**DO NOT translate**:
- YAML keys (`info`, `paths`, `get`, `post`, `parameters`, `responses`, `schema`, etc.)
- API endpoint paths (`/api/v1/users`)
- HTTP methods (`GET`, `POST`, `PUT`, `DELETE`)
- Parameter names (`room_id`, `user_name`)
- Schema property names
- Data type names (`string`, `integer`, `boolean`, `array`, `object`)
- Format values (`int64`, `date-time`)
- `$ref` references

#### $ref Translation

Translate the $ref path, change the zh to en.
```yaml
// Before
    AppId:
      $ref: "../../../../../snippets/common/zh/openapi/zego-shared-components.yaml#/components/parameters/AppId"

// After
    AppId:
      $ref: "../../../../../snippets/common/en/openapi/zego-shared-components.yaml#/components/parameters/AppId"
```


### JSON Translation Rules

Similar to YAML:
- Translate string values containing Chinese
- Keep JSON keys unchanged
- Preserve JSON structure and formatting

**Before**:
```json
{
  "title": "快速开始",
  "description": "这是一个示例描述：包含冒号"
}
```

**After**:
```json
{
  "title": "Quick Start",
  "description": "This is an example description: containing a colon"
}
```

## Quality Checklist

Before submitting translation, verify:

- [ ] All Chinese characters converted
- [ ] All Chinese punctuation converted
- [ ] Terminology matches reference table
- [ ] Code blocks unchanged (except comments)
- [ ] URLs unchanged
- [ ] Component names unchanged
- [ ] Formatting preserved
- [ ] Professional tone maintained
- [ ] No literal translations that sound awkward
- [ ] YAML values with colons use multi-line format (`|`)
- [ ] YAML/JSON structure and indentation preserved
- [ ] OpenAPI keywords kept unchanged
