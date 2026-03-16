---
name: translate-zh-to-en
description: This skill should be used when the user asks to "translate to English", "翻译成英文", "中译英", "translate this document", or requests to translate Chinese MDX/MD/json/yaml documentation to English. Triggers on translation requests for technical documentation files.
---

# Chinese to English Documentation Translation

Translate Chinese MDX/MD/json/yaml documentation files to English with professional quality and terminology consistency.

## Core Principles

### 1. Always Load Terminology Table

**Before translating each file**, load the terminology mapping tables in order:

1. **Common terminology**: `${doc_root}.translate/common-terminology.csv`
2. **Product-specific terminology** (if applicable): `${doc_root}.translate/products/<product>.csv`

Product identification based on file path:
- `real_time_video` / `real_time_voice` → `real_time_video_zh.csv`
- `zim` / `imkit` → `zim_zh.csv`
- `callkit` → `callkit_zh.csv`
- `live_streaming_kit` / `live_audio_room_kit` → `live_streaming_kit_zh.csv`
- `super_board` → `super_board_zh.csv`
- `ai_effects` → `ai_effects_zh.csv`

### 2. Skip Auto-Generated Files

**Do NOT translate** files where frontmatter contains `api` field:

```mdx
---
id: some-api
api: some/path  # ← Has 'api' field, SKIP this file
---
```

These MDX files are auto-generated from OpenAPI YAML specs.

### 3. Manual Translation Only

**STRICTLY FORBIDDEN**:
- Writing scripts for batch translation
- Using translation APIs
- Any automated translation tools

Translate each file manually, word by word, regardless of file count or size.

### 4. Translation Scope

**Translate**:
- Prose descriptions and explanations
- Table cell contents
- Image alt text
- Code comments (// and /* */ style)
- Frontmatter values (not keys)

**DO NOT translate**:
- Code blocks (code logic stays unchanged)
- URLs and links
- API endpoints
- Technical identifiers (variable names, function names)
- Parameter names
- MDX/JSX component names
- Frontmatter keys

### 5. Format Preservation

Maintain all original formatting:
- Markdown syntax (headings, lists, bold, italic)
- Table structures
- MDX/JSX component syntax
- Code block language specifiers
- Indentation and whitespace

## Translation Process

1. **Check frontmatter**: If contains `api` field, skip and report
2. **Load terminology**: Read common and product-specific CSV files
3. **Translate content**: Apply terminology, translate prose and comments
4. **Convert punctuation**: Chinese punctuation → English punctuation
   - `。` → `.`
   - `，` → `,`
   - `：` → `:` (except in YAML keys)
   - `（）` → `()`
   - `《》` → `""`
5. **Add spacing**: Space between English words and punctuation
6. **Verify**: No Chinese characters or punctuation in output

## Quality Standards

- Technical accuracy over literal translation
- Professional tone suitable for developer documentation
- Consistent terminology throughout document
- Clear and concise English

## Critical Rules (Most Common Errors)

### 1. Preserve MDX Closing Tags

**ALWAYS keep paired tags** - Never drop closing tags:

```mdx
// Before
<Note title="说明">
这是说明内容。
</Note>

// After (CORRECT)
<Note title="Description">
This is the note content.
</Note>

// WRONG - Missing closing tag
<Note title="Description">
This is the note content.
```

### 2. No Content Expansion

Translate faithfully, do NOT expand or embellish:

```
原文: 点击按钮
WRONG: Please click on the button that is located at the bottom right corner
CORRECT: Click the button
```

### 3. No Chinese Residue

Output MUST NOT contain any Chinese characters or punctuation:

```
WRONG: This is a test，please note.
CORRECT: This is a test, please note.
```

### 4. YAML Colon Handling

If translated value contains `:`, use multi-line format with `|`:

```yaml
// WRONG - YAML parser will fail
description: Interface name: Get user list

// CORRECT
description: |
  Interface name: Get user list
```

## Additional Resources

For detailed translation patterns and edge cases, see `references/translation-patterns.md`.
