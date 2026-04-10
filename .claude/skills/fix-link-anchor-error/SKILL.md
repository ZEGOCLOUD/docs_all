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

**Client API Document Detection**:

Before running the full anchor collection (Step 2), run a fast check to detect if the target file is a client API document:

```bash
python3 ./scripts/collect-valid-anchors.py <target-mdx-file-path> --has-param-field
```

Returns `{"has_param_field": true}` or `{"has_param_field": false}`.

- If `true` → this is a client API document. **Skip Steps 2–4 entirely** and go directly to **Step 5**.
- If `false` → proceed with Step 2 (collect anchors) as normal.

### 2. Collect Anchors from Target File

2.1. 初次收集目标文件中的锚点信息
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
When `count > 100`, the script returns only the first 100 anchors.

Anchor types:
- `md_heading` — Markdown `#` heading
- `a_tag` — HTML `<a id="...">` tag
- `h_tag` — HTML `<h1>`–`<h6>` tag with `id` attribute
- `step` — `<Step>` component (only when `titleSize` is h1–h5)
- `param_field` — `<ParamField>` component

2.2. 将所有 md_heading 类型的锚点转换成英文（如果包含中文）并写回原始文档中
如果返回结果中的 md_heading 包含中文字符，那么应该生成英文锚点然后调用 add-anchor.py 插入到文档中：
```bash
python3 ./scripts/add-anchor.py <target-mdx-file> \
  --type <anchor.type> \
  --value <anchor.value> \
  --new-id <english-anchor-name>
```
2.3. 重新收集目标文件中的锚点信息
重要！！：在所有 md_heading 都处理成英文锚点后，重新运行一次 `python3 ./scripts/collect-valid-anchors.py <target-mdx-file-path>` 获取最新的锚点数据再进行后续的语义匹配和链接替换。
如果重新收集后的锚点列表中仍然存在中文锚点，继续进行步骤 2.2 的处理过程。


**Note**: For external links, heading collection is not possible (skip to step 3 with provided anchors or user input). For pure internal page anchors, use the source file itself as the target.


### 3. Semantic Match and Replace

For each broken link, extract **two signals** and compare each against every collected anchor's `value`:

- **Anchor text**: the fragment part of the URL (e.g., `#getcurrentprogress-zegomediaplayer` → `"getcurrentprogress-zegomediaplayer"`)
- **Link display text**: the visible label in the markdown (e.g., `[获取当前播放进度](...)` → `"获取当前播放进度"`)

The final score for each candidate anchor is the **maximum** of its score against the anchor text and its score against the link display text. Either signal alone is enough to constitute a high-confidence match.

**Scoring rules** (normalize both sides: lowercase, remove special chars, spaces → hyphens):

| Condition | Score |
|-----------|-------|
| Exact match after normalization | 100 |
| Case / spacing / punctuation difference only | 90 |
| Chinese ↔ English semantic equivalence (cross-language) | 85–95 |
| Partial match or contains key terms | 60–80 |
| No meaningful overlap | < 60 |

Based on the best match score, apply the corresponding action:

| Score | Confidence | Action |
|-------|-----------|--------|
| **≥ 80** | High | Auto-fix: replace the broken anchor with the matched anchor's `value` in the source file |
| **60–80** | Medium | Present candidate to user for confirmation, then apply fix |
| **< 60** | Low | Report to user, do not modify |

**For `step` and `param_field` types** (`add-anchor.py` does not support these):
- Directly replace the broken anchor with the matched anchor's `value` as-is. The Chinese anchor value is acceptable — no need to convert to English.

### 4. Global Search and Replace

After fixing an anchor, the same broken link may appear in multiple files. Use `./scripts/replace-link.py` to propagate the fix globally — **but only for internal URL path links and pure page anchors**:

| Link type | Example | Global replace? |
|-----------|---------|----------------|
| Internal URL path | `/instance/path#old-anchor` | ✅ Safe |
| Pure page anchor | `#old-anchor` | ✅ Safe |
| Relative link | `./file.mdx#old-anchor` | ❌ Do NOT — same relative path resolves differently per directory |

For supported link types, first detect the language of the **source file** that contains the broken link:
- Path contains `/zh/` or `_zh` → Chinese file → pass `--zh`
- Otherwise → English file → no `--zh` flag

```bash
# Preview first
python3 ./scripts/replace-link.py <old-link> <new-link> [--zh] --dry-run
# Apply
python3 ./scripts/replace-link.py <old-link> <new-link> [--zh]
```

**Relative links with broken anchors must be fixed manually in each affected file.**

### 5. Client API Document — ParamField Anchor Fix

> This step is only reached from **Step 1** (when `param_field` anchors are detected). Steps 3–4 are skipped entirely.

Client API documents must **never be modified** — only the link in the source file is updated.

Run `--search-param-field` on the target file to find matching anchors:

```bash
python3 ./scripts/collect-valid-anchors.py <target-mdx-file> --search-param-field <broken-anchor-id>
```

Example:
```bash
python3 ./scripts/collect-valid-anchors.py ./class.mdx --search-param-field loadresourceaudioeffectidcallback-zegomediaplayer
```

Returns:
```json
{
  "matches": [
    "loadresourceaudioeffectidcallback",
    "loadresourceaudioeffectidcallback-zegoaudioeffectplayer",
    "loadresourceaudioeffectidcallback-zegoaudioeffectplayer-class"
  ]
}
```

The script uses a 3-level fallback strategy:
1. **Exact match**: search the broken anchor as-is
2. **Remove last `-` segment** (e.g., drop `-class`): search again
3. **Continue removing** `-` segments until a match is found

When multiple matches are returned, the agent should select the one that is **semantically closest** to the broken anchor (considering the parent class name in the link context).

**Rules for client API anchors:**
- ✅ Replace the broken anchor in the **source file only** (the file with the broken link)
- ❌ Do NOT modify the target API document file
- ❌ Do NOT run global search and replace (no Step 4)

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

**Broken link**: `[Prerequisites](/aiagent-android/quick-start#1_2)`

**Steps**:
1. Resolve URL: `python3 .docuo/scripts/config_helper.py --resolve-url /aiagent-android/quick-start`
2. Find file: `core_products/aiagent/zh/android/quick-start.mdx`
3. Add anchor: `## 前提条件 <a id="prerequisites" />`
4. Display text similar meaning: `prerequisites`
5. Fix link: `[Prerequisites](/aiagent-android/quick-start#prerequisites)`

### Example 3: Step Component

**Broken link**: `[Digital Human Intro](#digital-human)`

**Heading found**: `<Step title="数字人介绍" titleSize="h2">`

**Action**:
- Normalize "数字人介绍" → use as-is or generate pinyin-based ID
- Replace with: `[Digital Human Intro](#数字人介绍)`

### Example 4: Client API Document (ParamField)

**Broken link**: `[loadResource:audioEffectID:callback:](./class.mdx#loadresourceaudioeffectidcallback-zegomediaplayer)`

**Step 1**: Collect anchors from `./class.mdx` → contains `param_field` type → detected as client API doc.

**Step 5**: Run search:
```bash
python3 ./scripts/collect-valid-anchors.py ./class.mdx --search-param-field loadresourceaudioeffectidcallback-zegoexpressengine
```

Result: `["loadresourceaudioeffectidcallback", "loadresourceaudioeffectidcallback-zegoaudioeffectplayer", "loadresourceaudioeffectidcallback-zegoaudioeffectplayer-class"]`

Agent selects `loadresourceaudioeffectidcallback-zegoaudioeffectplayer`.

**Fix**: Update only the source file's link:
`[loadResource:audioEffectID:callback:](./class.mdx#loadresourceaudioeffectidcallback-zegoaudioeffectplayer)`

## Related Scripts

- `${doc_root}/.docuo/scripts/config_helper.py` — Core utility for URL/file path resolution
- `./scripts/collect-valid-anchors.py` — Collect all valid anchors from an MDX file (with type info)
- `./scripts/add-anchor.py` — Insert a new anchor ID into a specific element in an MDX file
- `./scripts/replace-link.py` — Global search and replace anchor links (internal URL paths and pure anchors only; rejects relative links)

## Notes

- Only processes anchors in **relative links** and **internal links**
- For URL path (internal) links, first resolves to local file using `config_helper.py`
- For relative links, calculate the absolute path using the source file's(which is the file that contains the broken link) directory: `path.resolve(source_file_dir, relative_path)`
- Step components are handled specially - they use the `title` attribute directly as anchor
- Anchor IDs are typically lowercase with hyphens for spaces
- Chinese headings may use pinyin or the original characters as anchor IDs
