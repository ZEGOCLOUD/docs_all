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

### 2. Collect Anchors from Target File

Run the `collect-valid-anchors.py` script on the target file to get all valid anchors:

```bash
python3 ./scripts/collect-valid-anchors.py <target-mdx-file-path>
```

The script outputs a JSON object:

```json
{
  "count": 12,
  "anchors": [
    { "type": "md_heading", "value": "quick-start" },
    { "type": "a_tag",      "value": "prerequisites" },
    { "type": "h_tag",      "value": "api-ref" },
    { "type": "step",       "value": "integrate-sdk" },
    { "type": "param_field","value": "room-id" }
  ]
}
```

Anchor types:
- `md_heading` — Markdown `#` heading
- `a_tag` — HTML `<a id="...">` tag
- `h_tag` — HTML `<h1>`–`<h6>` tag with `id` attribute
- `step` — `<Step>` component (only when `titleSize` is h1–h5)
- `param_field` — `<ParamField>` component

When `count > 100`, the script returns only the first 100 anchors.

**Note**: For external links, heading collection is not possible (skip to step 3 with provided anchors or user input). For pure internal page anchors, use the source file itself as the target.

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

Compare the broken anchor text against the anchors collected in step 2.
Apply the **first matching rule** below:

#### Rule A — High string similarity (> 90%)

If any collected anchor's `value` has **string similarity > 90%** with the broken anchor (case-insensitive, after normalizing hyphens/underscores/spaces), replace the broken anchor directly with that `value`. No file modification needed.

#### Rule B — Same meaning across Chinese / English

If no Rule A match, check whether any collected anchor has the **same semantic meaning** as the broken anchor when compared across Chinese and English (e.g., `#prerequisites` broken → collected anchor value `前提条件` in a Chinese heading). When a match is found:

1. Decide the **English anchor name** (e.g., `prerequisites`) — must be ASCII only, lowercase, hyphens for spaces.
2. Call `add-anchor.py` to insert the anchor into the target MDX file:

```bash
python3 ./scripts/add-anchor.py <target-mdx-file> \
  --type <anchor.type> \
  --value <anchor.value> \
  --new-id <english-anchor-name>
```

3. Replace the broken anchor in the source file with the new English anchor name.

> **Note**: `step` and `param_field` types are not supported by `add-anchor.py`. For these types, skip the `add-anchor.py` call and directly replace the broken anchor with the matched anchor's `value` (the Chinese anchor value is acceptable — no need to convert to English).

#### Rule C — No meaningful match

If neither Rule A nor Rule B applies (no anchor with similar or equivalent meaning exists), **remove the anchor fragment** from the link and convert it to plain text or a link without anchor.

Example: `[Prerequisites](#prerequisites)` → `Prerequisites` (plain text) or `[Prerequisites](./quick-start.mdx)` (link without anchor).

### 5. Apply Fix

Update the source file to replace the broken anchor with the corrected one.

### 6. Global Search and Replace

For **relative links** and **internal links**, the same broken anchor may appear in multiple files across the repo. After fixing the anchor, run `replace-anchor.py` to propagate the change globally:

```bash
python3 ${doc_root}/.scripts/check/replace-link.py <old-link> <new-link>
```

- `<old-link>` — the exact broken link as it appears in files, including the anchor fragment (e.g., `./some-file.mdx#old-anchor` or `/instance/path#old-anchor`)
- `<new-link>` — the corrected full link with the new anchor (e.g., `./some-file.mdx#new-anchor`)

The script searches all `.mdx`, `.md`, `.yaml`, `.yml` files in the repo and replaces every exact occurrence.

Use `--dry-run` first to preview affected files before writing:

```bash
python3 ${doc_root}/.scripts/check/replace-link.py <old-link> <new-link> --dry-run
```

**Note**: This step applies to relative and internal links only. Pure page-internal anchors (`#anchor`) are file-specific and should not be globally replaced.

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

- `${doc_root}/.docuo/scripts/config_helper.py` — Core utility for URL/file path resolution
- `./scripts/collect-valid-anchors.py` — Collect all valid anchors from an MDX file (with type info)
- `./scripts/add-anchor.py` — Insert a new anchor ID into a specific element in an MDX file
- `${doc_root}/.scripts/check/replace-link.py` — Global search and replace a link across the entire repo (shared with fix-internal-link-error skill)

## Notes

- Only processes anchors in **relative links** and **internal links**
- For URL path (internal) links, first resolves to local file using `config_helper.py`
- For relative links, calculate the absolute path using the source file's(which is the file that contains the broken link) directory: `path.resolve(source_file_dir, relative_path)`
- Step components are handled specially - they use the `title` attribute directly as anchor
- Anchor IDs are typically lowercase with hyphens for spaces
- Chinese headings may use pinyin or the original characters as anchor IDs
