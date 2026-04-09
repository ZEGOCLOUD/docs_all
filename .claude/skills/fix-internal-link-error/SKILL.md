---
name: fix-internal-link-error
description: "This skill fixes broken internal links in MDX documentation files. Use when fixing 404 errors, dead links, or URL paths that point to deleted/renamed files. Supports markdown links, HTML 'a' tags, and React components like Link, Card, and Button. 触发短语: 'fix internal link', '修复内部链接', 'broken link', '断链', '404 link', '404链接', 'dead link', '死链', 'fix link error', '修复链接错误'."
---

# fix-internal-link-error

This skill fixes internal link errors in documentation files. When an internal link (URL path) points to a non-existent file (usually because the file was renamed or deleted), this skill helps find the correct target and update the link.

## Workflow

### Step 1: Resolve the URL to find the expected file path

```bash
python3 ${doc_root}/.docuo/scripts/config_helper.py --resolve-url /docs/zim-android/introduction/overview
```

This will return the expected file path if the file exists, or indicate the file is not found.

### Step 2: Get instance information

```bash
python3 ${doc_root}/.docuo/scripts/config_helper.py --info /path/to/file.mdx
```

This returns the instance's `routeBasePath` and `path` (instance directory).

### Step 3: Read sidebars.json

Read the `sidebars.json` file from the instance directory to get all valid file IDs and their labels.

### Step 4: Calculate match scores

**Label matching:**
- Extract the link label (e.g., "Overview") from the markdown/a tag/component
- Search all sidebar nodes for matching labels
- Exact label match: 60 points
- Case/spacing/punctuation difference: 50 points (-10)

**Path matching:**
- Extract the link path and remove the `routeBasePath` to get the relative file target
- Compare with each sidebar node's `id`:
  - Directory prefix match: +20 points
  - Semantic similarity (filename part): +10~20 points

### Step 5: Apply fix based on confidence

- **High confidence (>90)**: Automatically update the file
- **Medium confidence (60-90)**: Present options to user
- **Low confidence (<60)**: Report issue, do not modify

### Step 6: Global Search and Replace

The same broken link may appear in multiple files across the repo. After confirming the correct replacement, run `replace-link.py` to propagate the fix globally:

```bash
python3 ${doc_root}/.scripts/check/replace-link.py <old-link> <new-link>
```

- `<old-link>` — the exact broken link as it appears in files (complete link, may include anchor fragment)
- `<new-link>` — the corrected link (complete link, may include anchor fragment)

The script searches all `.mdx`, `.md`, `.yaml`, `.yml` files in the repo and replaces every exact occurrence.

Use `--dry-run` first to preview affected files before writing:

```bash
python3 ${doc_root}/.scripts/check/replace-link.py <old-link> <new-link> --dry-run
```


## Example

Given a broken link `[Overview](/real-time-video-android-java/introduction/overview)`:

1. Extract target: `introduction/overview`
2. Find all file IDs from sidebars.json:
   - `introduction/entry` (label: "Entry")
   - `introduction/overview-new` (label: "Overview") ← Exact match!
   - `introduction/product-feature-list` (label: "Product Feature List")
3. Score `introduction/overview-new`: 98
4. Replace the URL with `/real-time-video-android-java/introduction/overview-new`


## Related Scripts

- `${doc_root}/.docuo/scripts/config_helper.py` — Core utility for URL/file path resolution
- `${doc_root}/.scripts/check/replace-link.py` — Global search and replace a broken link across the entire repo

## Notes

- The skill uses semantic matching to handle cases where files have been slightly renamed
- Numeric prefixes (e.g., `01-`, `02-`) are ignored during matching
- The `routeBasePath` from the instance configuration is always preserved in the replacement
- Only `.mdx` and `.md` files are considered
