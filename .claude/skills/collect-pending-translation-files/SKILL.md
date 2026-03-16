---
name: collect-pending-translation-files
description: This skill should be used when the user asks to "translate a product", "translate a platform", "translate a folder", "翻译某个产品", "翻译某个平台", "翻译某个文件夹", "collect files for translation", "scan directory for translation", "collect pending translation files", "扫描待翻译文件". Use when the user specifies a directory or product to translate and needs to identify which files need translation.
---

# Collect Pending Translation Files

Scan English documentation directories to find files that still contain Chinese characters (incomplete translations). Unlike `collect-git-changes-for-translation` which analyzes git diff, this skill scans directories directly to find untranslated or partially translated files.

## Purpose

Identify English documentation files that still contain Chinese characters, indicating they need translation or have incomplete translations. Automatically skips:
- API documentation (docType: API)
- Full reuse documents (import Content pattern)
- Lock files and node_modules

## How It Works

The script detects whether the input directory is Chinese (`/zh/`) or English (`/en/`):

1. **Chinese directory input** → Automatically finds corresponding English directory → Scans English files for Chinese characters
2. **English directory input** → Directly scans for Chinese characters

A file is considered "pending translation" if it contains Chinese characters `[\u4e00-\u9fff]` in the English version.

## Usage

Always output to a file to preserve context for LLM agents:

```bash
# Scan Chinese directory (auto-finds English dir)
python3 scripts/scan_pending_translation.py core_products/aiagent/zh -o /tmp/docs-pending-translation-$(date +%Y%m%d%H%M%S).json

# Scan English directory directly
python3 scripts/scan_pending_translation.py core_products/aiagent/en -o /tmp/docs-pending.json

# From any directory with explicit docs root
python3 scripts/scan_pending_translation.py /path/to/dir --docs-root /path/to/docs -o /tmp/pending.json
```

### Arguments

| Argument | Description |
|----------|-------------|
| `directory` | 目录路径（中文目录或英文目录） |
| `--docs-root` | 文档根目录（用于计算相对路径，默认为当前目录） |
| `-o, --output` | 输出文件路径（推荐） |

### Examples

**Scenario 1: Scan specific directory**
```
User: "翻译这个路径下的文件 core_products/aiagent/en"
Action: Scan core_products/aiagent/en for Chinese characters
```

```bash
python3 scripts/scan_pending_translation.py core_products/aiagent/en -o /tmp/docs-pending-translation-$(date +%Y%m%d%H%M%S).json
```

**Scenario 2: Scan a product**
```
User: "Check what needs translation in AIAgent docs"
Action: Scan core_products/aiagent/en for Chinese characters
```

```bash
python3 scripts/scan_pending_translation.py core_products/aiagent/en -o /tmp/docs-pending.json
```

**Scenario 3: Scan a platform of a product**
```
User: "翻译实时音视频 Flutter 平台的文档"
Action: Scan the Flutter subdirectory of real-time-voice-video
```

```bash
python3 scripts/scan_pending_translation.py core_products/real-time-voice-video/zh/flutter -o /tmp/pending.json
```

## Output Format

The script outputs JSON with precise line numbers for agent navigation:

```json
{
  "success": true,
  "input_directory": "core_products/aiagent/zh",
  "check_directory": "core_products/aiagent/en",
  "mode": "zh_to_en",
  "directory_exists": true,
  "total_files": 20,
  "details": [
    {
      "path": "core_products/aiagent/en/server/quick-start.mdx",
      "chinese_chars": 14,
      "lines": ["23", "64"]
    },
    {
      "path": "core_products/aiagent/en/server/guides/config.mdx",
      "chinese_chars": 150,
      "lines": ["1~30", "45", "100~120"]
    }
  ]
}
```

**`lines` format:**
- Single line: `"23"`
- Consecutive range: `"15~30"` (lines 15 through 30)

This allows agents to quickly locate and translate specific lines without reading the entire file.

## Supported File Types

- `.md` - Markdown files
- `.mdx` - MDX files
- `.json` - JSON files
- `.yaml` / `.yml` - YAML files

## Automatic Filtering

| Category | Action |
|----------|--------|
| API documentation (docType: API) | Skip - no translation needed |
| Full reuse documents (import Content) | Skip - handled by reuse process |
| Lock files (package-lock, yarn.lock, etc.) | Skip |
| node_modules, .docusaurus | Skip |

## Workflow

1. **Confirm the directory to scan**
   Determine the target directory based on user's request (product name, platform, or specific folder path).

2. **Run script with output file**
   ```bash
   python3 scripts/scan_pending_translation.py <directory> -o /tmp/docs-pending-translation-$(date +%Y%m%d%H%M%S).json
   ```

3. **Review results**
   ```bash
   cat /tmp/docs-pending-translation-*.json | jq '.files'
   ```

## Common Product/Platform Paths

| User Request | Typical Path |
|--------------|--------------|
| AIAgent | `core_products/aiagent/zh` |
| Real-time Voice/Video | `core_products/real-time-voice-video/zh` |
| Live Streaming | `core_products/live-streaming/zh` |
| ZIM | `core_products/zim/zh` |
| Call Kit | `uikit_kits/call-kit/zh` |
| Live Audio Room Kit | `uikit_kits/live-audio-room-kit/zh` |

## Key Principle

**Always output to file** - This preserves the file list outside of LLM context, allowing agents to reference it later without keeping hundreds of file paths in memory.
