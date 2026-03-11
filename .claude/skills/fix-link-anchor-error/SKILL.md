---
name: fix-link-anchor-error
description: "This skill fixes broken anchor links in MDX documentation files. Use when anchor links point to invalid or non-existent anchor IDs. Handles anchor errors in markdown links, HTML 'a' tags, and React components like Link, Button, and Card. 触发短语: 'fix anchor link', '修复锚点链接', 'broken anchor', '锚点错误', 'anchor not found', '找不到锚点', 'invalid anchor', '无效锚点'."
---

# fix-link-anchor-error

This skill fixes broken anchor links in documentation files. Anchor links are used to jump to specific sections within a page (e.g., `[Prerequisites](#prerequisites)`). When an anchor link points to a non-existent or incorrect anchor ID, this skill helps find the correct heading and fix the anchor.

## Supported Link Types

This skill handles anchor errors in:

1. **Relative links**: `[Text](./some-file.md#anchor-id)` - Anchor points to a section in another local file
2. **Internal links** (URL path): `[Text](/instance/path/to/file#anchor-id)` - First resolve to local file, then fix anchor
3. **Pure internal page anchors**: `[Text](#anchor)` - Anchor points to a section in the same file. Start from step 2.

**Note**: External links (`https://...`) cannot be fixed since we cannot modify external sites. Only semantic matching suggestions can be provided.


## How it works

### 1. Identify the Link Type and Target File

- **Relative link**:
  1. Extract the relative file path from the URL (e.g., `./some-file.md#anchor` → `./some-file.md`)
  2. Calculate the absolute path using the source file's(which is the file that contains the broken link) directory: `path.resolve(source_file_dir, relative_path)`
  3. Open the file at the absolute path and proceed to collect headings
- **External link**: The target is the external URL itself (cannot collect headings, skip to step 3 for semantic matching only)
- **Internal link (URL path)**: Use `config_helper.py --resolve-url` to find the local file
- **Pure internal page anchor**: The target is the current source file itself

```bash
# For URL path links, resolve to local file
python3 ${doc_root}/.docuo/scripts/config_helper.py --resolve-url <url-path or url>
```

### 2. Collect Headings from Target File

Scan the target file for all headings:

- **Markdown headings**: `## Heading Text`, `### Heading Text`, etc. (h1-h5)
- **Step components**: `<Step title="Heading Text">` or `<Step titleSize="h2" title="Heading Text">`

Also detect special heading wrappers:
- `<Steps titleSize="h3">` with child `<Step title="...">` or `<Step titleSize="h2" title="...">`

**Note**: For external links, heading collection is not possible (skip to step 3 with provided headings or user input). For pure internal page anchors, use the source file itself as the target.

### 3. Semantic Matching

Extract the anchor text from the broken link (e.g., `#prerequisites` → "prerequisites") and compare with collected headings:

1. **Normalize both strings**:
   - Convert to lowercase
   - Remove special characters
   - Replace spaces with hyphens

2. **Calculate similarity score**:
   - Exact match (after normalization): 100 points
   - Case difference only: -10 points
   - Minor spacing/punctuation difference: -10 points
   - Partial match (contains key terms): 60-80 points

3. **Score threshold**:
   - **> 90 points**: High confidence, auto-fix
   - **60-90 points**: Medium confidence, present options to user
   - **< 60 points**: Low confidence, report to user

### 4. Check or Generate Anchor ID

For the matched heading:

1. **Check if anchor already exists**:
   - Look for `<a id="anchor-id" />` or `<a id="anchor-id"></a>` next to the heading
   - Example: `## 前提条件 <a id="prerequisites" />`

2. **If anchor exists**: Use the existing anchor ID to replace the broken one

3. **If anchor doesn't exist**:
   - **For standard headings (h1-h5)**:
     - Generate anchor ID from heading text (lowercase, spaces to hyphens, remove special chars)
     - Insert `<a id="generated-id" />` after the heading text or on the next line
     - Use the generated ID to replace the broken anchor
   - **For `<Step>` components**:
     - Step components don't support `<a id>` tags
     - Use the `title` attribute value directly (after normalization) as the anchor ID
     - Replace the broken anchor with the normalized title

### 5. Apply Fix

Update the markdown file to replace the broken anchor with the corrected one.

## Example

### Example 1: Relative Link with Broken Anchor

**Broken link**: `[Prerequisites](./quick-start.md#precondition)`

**Target file**: `./quick-start.md`

**Headings found in target file**:
- `## 前提条件 <a id="prerequisites" />`
- `### Installation`
- `## Quick Start`

**Matching**:
- "precondition" vs "prerequisites" → Similar meaning, score: 85
- "precondition" vs "Installation" → Not similar, score: 30

**Action**: Present option to user - "Did you mean `#prerequisites`?"

### Example 2: URL Path Link with Missing Anchor

**Broken link**: `[Prerequisites](/aiagent-android/quick-start#prerequisites)`

**Steps**:
1. Resolve URL: `python3 .docuo/scripts/config_helper.py --resolve-url /aiagent-android/quick-start`
2. Find file: `core_products/aiagent/zh/android/quick-start.mdx`
3. Find heading: `## 前提条件` (no anchor)
4. Generate anchor: `prerequisites`
5. Add anchor: `## 前提条件 <a id="prerequisites" />`
6. Fix link: `[Prerequisites](/aiagent-android/quick-start#prerequisites)`

### Example 3: Step Component

**Broken link**: `[Digital Human Intro](#digital-human)`

**Heading found**: `<Step title="数字人介绍" titleSize="h2">`

**Action**:
- Normalize "数字人介绍" → use as-is or generate pinyin-based ID
- Replace with: `[Digital Human Intro](#数字人介绍)` or `[Digital Human Intro](#shu-zi-ren-jie-shao)`

## Related Scripts

- `${doc_root}/.docuo/scripts/config_helper.py` - Core utility for URL/file path resolution

## Notes

- Only processes anchors in **relative links** and **internal links**
- For URL path (internal) links, first resolves to local file using `config_helper.py`
- For relative links, calculate the absolute path using the source file's(which is the file that contains the broken link) directory: `path.resolve(source_file_dir, relative_path)`
- Step components are handled specially - they use the `title` attribute directly as anchor
- Anchor IDs are typically lowercase with hyphens for spaces
- Chinese headings may use pinyin or the original characters as anchor IDs
