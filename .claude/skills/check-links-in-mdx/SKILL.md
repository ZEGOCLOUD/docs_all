---
name: check-links-in-mdx
description: "This skill checks whether links in MDX documentation files are valid. Use when the user wants to validate links in a single MDX file or all files under a documentation instance. 触发短语: 'check links', '检查链接', 'validate links', '验证链接', 'find broken links', '查找断链', 'check for link errors', '检查链接错误', 'run link checker', '运行链接检查'."
---

# check-links-in-mdx

Check whether links in MDX documentation files are valid by running the link checker script.

## How to use

This skill runs the link checker script non-interactively to validate links in MDX files.

### Remove old link check results

```bash
rm -rf .scripts/check/check_link_result.json
```

### Check all links in an instance

```bash
python3 .scripts/check/check_links.py --zh --instance "<instance-id>"
```
You can pass the instance path to the script instead of the instance ID.

```bash
python3 .scripts/check/check_links.py --zh --instance-path "<path-to-instance>"
```

### Check links in a specific file

```bash
python3 .scripts/check/check_links.py --zh --file "<path-to-file.mdx>"
```

### Check links with remote URL validation

```bash
python3 .scripts/check/check_links.py --zh --instance "<instance-id>" --remote
```

**Arguments:**
- `--zh` / `--en`: Language option (`--zh` for Chinese, `--en` for English)
- `--instance`: Instance ID to check (use exact instance name from docuo config)
- `--file`: Specific MDX file path to check (relative to repo root or absolute)
- `--remote`: Also check remote external links (slower, requires network)

**Output:**
- Console output with categorized link issues
- Results saved to `${doc_root}/.scripts/check/check_link_result.json`

## Example

```bash
# Check all links in the macOS Objective-C real-time video instance
python3 .scripts/check/check_links.py --zh --instance real_time_video_ios_oc_zh

# Check a specific file
python3 .scripts/check/check_links.py --zh --file "core_products/real-time-voice-video/zh/macos-oc/client-sdk/api-reference/function-list.mdx"

# Check with remote URL validation
python3 .scripts/check/check_links.py --zh --instance real_time_video_ios_oc_zh --remote
```

## How it works (internal)

1. Read docuo config file (zh/en) based on language argument
2. Load instances from config and validate the provided instance ID
3. Scan MDX files and extract all links (anchor, internal, external, relative)
4. Validate each link type:
   - **Anchor links**: Check if target heading/ParamField anchor exists in target file
   - **Internal links**: Verify target MDX file exists with URL path
   - **Relative links**: Resolve path and verify file exists
   - **External links** (--remote only): HTTP request to verify accessibility
5. Categorize issues by type:
   - Invalid anchor links
   - Broken internal links
   - Language mixing (Chinese doc with zegocloud.com or English doc with zego.im)
   - Unreachable external links
6. Save results to `check_link_result.json` with categorized issues

## Getting instance IDs

To find available instance IDs, read the docuo config file:
- Chinese: `docuo.config.zh.json` → `instances` array
- English: `docuo.config.en.json` → `instances` array

Each instance has an `id` field that can be passed to `--instance`.
