---
name: fix-internal-link-error
description: "This skill fixes broken internal links in MDX documentation files. Use when fixing 404 errors, dead links, or URL paths that point to deleted/renamed files. Supports markdown links, HTML 'a' tags, and React components like Link, Card, and Button. 触发短语: 'fix internal link', '修复内部链接', 'broken link', '断链', '404 link', '404链接', 'dead link', '死链', 'fix link error', '修复链接错误'."
---

# fix-internal-link-error

This skill fixes internal link errors in documentation files. When an internal link (URL path) points to a non-existent file (usually because the file was renamed or deleted), this skill helps find the correct target and update the link.

## Workflow

### Step 1: Identify the target instance by routeBasePath

Internal links are often cross-instance. The `routeBasePath` prefix of the URL is usually correct — only the path **after** it is broken. Use `--match-route` to identify the target instance:

```bash
python3 ${doc_root}/.docuo/scripts/config_helper.py --match-route <broken-url-path>
```

Example:
```bash
python3 ${doc_root}/.docuo/scripts/config_helper.py --match-route /real-time-video-android-java/introduction/error-overview
```

Example return value:
```json
{
  "id": "real_time_video_android_java_zh",
  "label": "实时音视频 (Android Java)",
  "path": "core_products/real-time-voice-video/zh/android-java",
  "clientApiPath": "client-sdk/api-reference",
  "routeBasePath": "real-time-video-android-java",
  "locale": "zh"
}
```

- **Returns instance info** → `routeBasePath` is valid; proceed to Step 2.
- **Returns `null`** → the `routeBasePath` itself is unknown. List all valid base paths for reference:

```bash
python3 ${doc_root}/.docuo/scripts/config_helper.py --list-routes
```

If the link's prefix doesn't match any known `routeBasePath`, report the issue to the user and stop.

### Step 2: Locate sidebars.json from the instance path

Step 1 already returns the `path` field of the matched instance. The `sidebars.json` is located at:

```
${doc_root}/${instance.path}/sidebars.json
```

For the example above, that would be:

```
${doc_root}/core_products/real-time-voice-video/zh/android-java/sidebars.json
```

Read this file directly — no additional script call needed.

### Step 3: Calculate match scores

Extract the path segment **after** the `routeBasePath` from the broken link (the part that's wrong). Compare it against every entry in `sidebars.json`:

**Label matching** (use the link's display text, e.g., "Overview"):
- Exact literal match: 90 points
- Semantic match (same meaning, e.g. across Chinese/English): 80 points

**Path matching** (bonus on top of the label score, compare the broken path suffix against the sidebar `id`):
- Semantic match on the filename segment: +10~20 points

### Step 4: Apply fix based on confidence

- **High confidence (> 90)**: Automatically update the file
- **Medium confidence (70–90)**: Present top candidates to user for confirmation
- **Low confidence (< 70)**: Report the issue, do not modify

### Step 5: Global Search and Replace

The same broken link may appear in multiple files across the repo. After confirming the correct replacement, run `replace-link.py` to propagate the fix globally.

First detect the language of the **source file** that contains the broken link:
- Path contains `/zh/` or `_zh` → Chinese file → pass `--zh`
- Otherwise → English file → no `--zh` flag

```bash
# Preview first
python3 ./scripts/replace-link.py <old-link> <new-link> [--zh] --dry-run
# Apply
python3 ./scripts/replace-link.py <old-link> <new-link> [--zh]
```

- `<old-link>` — the exact broken link as it appears in files (complete link, may include anchor fragment)
- `<new-link>` — the corrected link (complete link, may include anchor fragment)

The script searches all `.mdx`, `.md`, `.yaml`, `.yml` files in the repo (filtered by language) and replaces every exact occurrence.


## Example

Given a broken link `[Overview](/real-time-video-android-java/introduction/overview)`:

1. Run `--match-route /real-time-video-android-java/introduction/overview` → returns instance `real-time-video-android-java` ✅
2. Run `--sidebars /real-time-video-android-java/introduction/overview` → get sidebars.json
3. Path after routeBasePath: `introduction/overview`. Compare against sidebar entries:
   - `introduction/entry` (label: "Entry")
   - `introduction/overview-new` (label: "Overview") ← label exact match + path prefix match → score 98 ✅
   - `introduction/product-feature-list` (label: "Product Feature List")
4. Auto-fix: replace with `/real-time-video-android-java/introduction/overview-new`


## Related Scripts

- `${doc_root}/.docuo/scripts/config_helper.py` — Core utility for URL/file path resolution
- `./scripts/replace-link.py` — Global search and replace a broken link across the entire repo

## Notes

- Internal links are typically cross-instance: the `routeBasePath` is the reliable part; only the path after it is broken.
- The `routeBasePath` is **always preserved** in the replacement — never change it.
- Numeric prefixes (e.g., `01-`, `02-`) are ignored during matching.
- Only `.mdx` and `.md` files are considered as targets.
