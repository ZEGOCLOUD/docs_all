---
name: api-short-link-to-mdx
description: >
  This skill resolves ZEGO API short links (e.g., [sendSEI](@sendSEI)) to the corresponding local
  API reference MDX file. Use when reading documentation that contains [text](@apiName) format links
  and the API details need to be checked. Triggers on: "resolve api short link", "find api mdx",
  "解析 @ 短链", "@短链解析", "API 短链", "find the mdx for @link", "resolve @ short link",
  "查看 API 短链对应的文档". Not needed for full URLs or URL paths (use url-to-mdx instead).
---

# api-short-link-to-mdx

Resolve a ZEGO API short link (`@apiName`) to the local API reference MDX file, so the API documentation can be read directly.

## When to use

Use this skill when encountering `[text](@apiName)` format links in ZEGO documentation, such as:
- `[startPublishingStream](@startPublishingStream)`
- `[sendSEI](@sendSEI)`
- `[ZegoExpressEngine](@-ZegoEngine)`

This is the `@` short link counterpart of the `url-to-mdx` skill (which handles URL paths like `/real-time-video-web/...`).

## How to use

Run the helper script:

```bash
bash ${SKILL_ROOT}/scripts/resolve.sh <short_link> <current_mdx_path>
```

**Arguments:**
- `short_link`: API name without the `@` sign (e.g., `startPublishingStream`, `sendSEI`)
- `current_mdx_path`: Path of the MDX file where the short link appears, relative to docs root

**Output** (4 lines on success):
1. instance ID (e.g., `real_time_video_web_zh`)
2. resolved URL path (e.g., `/real-time-video-web/client-sdk/api-reference/class#startpublishingstream`)
3. local MDX file absolute path
4. anchor slug for searching within the file

On failure, an error message is printed to stderr and the script exits with code 1.

## Examples

```bash
# Resolve a method short link
bash ${SKILL_ROOT}/scripts/resolve.sh startPublishingStream core_products/real-time-voice-video/zh/web/quick-start.mdx
# => real_time_video_web_zh
# => /real-time-video-web/client-sdk/api-reference/class#startpublishingstream
# => /path/to/docs_all/core_products/real-time-voice-video/zh/web/client-sdk/api-reference/class.mdx
# => startpublishingstream

# Resolve an enum/class heading link
bash ${SKILL_ROOT}/scripts/resolve.sh "-ZegoEngine" core_products/real-time-voice-video/zh/web/quick-start.mdx
```

After resolution, read the returned MDX file and search for the anchor slug to find the specific API documentation.

## Limitations

- Only works for documents under an instance that has `clientApiPath` configured in `docuo.config.json`
- Most core products (RTC, RTV, IM) have this configured; some solutions (KTV, etc.) may not
- If resolution fails, the `@` link may reference an API from a different product's instance — try resolving against a document from that product instead
