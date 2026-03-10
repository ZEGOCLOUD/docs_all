---
name: url-to-mdx
description: "This skill finds the local MDX source file for a ZEGO/ZEGOCLOUD documentation URL. Use when the user provides a doc URL and needs to find or edit the corresponding source file. 触发短语: 'edit this page', '编辑这个页面', 'find the mdx for this URL', '找到对应的mdx文件', 'locate source file', '定位源文件', 'open the mdx for', '打开mdx', 'convert URL to mdx', 'URL转mdx'. Triggers when user pastes URLs from doc-zh.zego.im, zegocloud.com/docs, or localhost:3000."
---

# url-to-mdx

Given a ZEGO/ZEGOCLOUD documentation page URL, find the corresponding local `.mdx` source file in a Docuo-based docs repository.

## How to use

Run the helper script with the docs root directory and the URL:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/find_mdx.py <docs_root> <url>
```

**Arguments:**
- `docs_root`: The directory containing `docuo.config.*.json` (the docs repository root)
- `url`: Full URL (`http://localhost:3000/...`, `https://doc-zh.zego.im/...`, `https://www.zegocloud.com/docs/...`) or path (`/real-time-video-ios-oc/...`)

**Output:** Absolute path to the matching `.mdx` (or `.md`) file, printed to stdout.
On failure, an error message is printed to stderr and the script exits with code 1.

## Example

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/find_mdx.py \
  /Users/name/zego_docs \
  "https://doc-zh.zego.im/real-time-video-ios-oc/introduction/overview"
# => /Users/name/zego_docs/core_products/real-time-voice-video/zh/ios-oc/introduction/overview.mdx
```

## Domain -> config file mapping

| Domain | Config file |
|--------|-------------|
| `doc-zh.zego.im` | `docuo.config.zh.json` |
| `*.zegocloud.com` | `docuo.config.en.json` |
| `localhost` or path only | `docuo.config.zh.json` |
| other | `docuo.config.json` |

## How it works (internal)

1. Parse the URL path and select the right config file based on domain.
2. Read `instances` from the config; each instance has `routeBasePath` and `path`.
3. Greedy-match the URL path against `routeBasePath` values (longest match wins).
4. Compute the remaining path after the matched prefix.
5. Recursively scan `.md`/`.mdx` files in the instance directory.
6. Normalize each file path to a `fileId` (strip extension, strip numeric prefixes like `01-`, lowercase, spaces to hyphens, strip trailing `/index`).
7. Return the file whose `fileId` matches the remaining URL path (lowercased).