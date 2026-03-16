---
name: collect-git-changes-for-translation
description: This skill should be used when the user asks to "collect changes for translation", "收集翻译文件", "what files need translation", "待翻译文件", "find files to translate", "查找待翻译文件", "analyze git changes", "分析改动", "translation file list". Use when the user needs to identify which documentation files have been modified and require translation.
---

# Collect Git Changes for Translation

Identify documentation files that have been modified in a git commit range and need translation. Outputs a minimal JSON file with file paths only.

## Purpose

Analyze git changes to generate a list of files that need translation. Automatically excludes English document paths defined in `docuo.config.en.json`.

## Usage

Always output to a file to preserve context for LLM agents:

```bash
# Standard usage - output to timestamped file
python3 scripts/analyze_translation_changes.py <docs_root> -o /tmp/docs-git-changes-$(date +%Y%m%d%H%M%S).json

# With commit range
python3 scripts/analyze_translation_changes.py <docs_root> -o /tmp/docs-git-changes.json HEAD~10 HEAD
```

### Arguments

| Argument | Description |
|----------|-------------|
| `docs_root` | 文档根目录路径（包含 docuo.config.en.json 的目录） |
| `-o, --output` | 输出文件路径（推荐） |
| `--repo PATH` | git 仓库路径（当不在仓库目录下执行时使用） |
| `start_commit` | 起始 commit hash 或分支名 |
| `end_commit` | 结束 commit hash，默认为 HEAD |

### Examples

**Scenario 1: In docs directory**
```bash
python3 scripts/analyze_translation_changes.py . -o /tmp/docs-git-changes-20260313.json
```

**Scenario 2: From any directory**
```bash
python3 scripts/analyze_translation_changes.py /path/to/docs -o /tmp/docs-git-changes-20260313.json
```

**Scenario 3: With specific commit range**
```bash
python3 scripts/analyze_translation_changes.py /path/to/docs -o /tmp/docs-git-changes.json abc123 def456
```

## Output Format

The script outputs minimal JSON for efficient LLM consumption:

```json
{
  "success": true,
  "range": "origin/main..HEAD",
  "docs_root": "/path/to/docs",
  "total_files": 5,
  "files": [
    "docs/guide.mdx",
    "docs/api.mdx"
  ],
  "excluded_english_paths": 42
}
```

## Supported File Types

- `.md` - Markdown files
- `.mdx` - MDX files
- `.json` - JSON files
- `.yaml` / `.yml` - YAML files

## Automatic Exclusions

- English document paths from `docuo.config.en.json`
- `/en/` directories
- `node_modules/`, `.docusaurus/`
- Lock files (`package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`)
- Snapshot files

## Workflow
1. **Confirm the range of changes**
   Determine the git commit range according to user requirements. If the user does not specify, the script will use the diff between the latest commit and the origin/main branch by default.

2. **Run script with output file**
   ```bash
   python3 scripts/analyze_translation_changes.py . -o /tmp/docs-git-changes-$(date +%Y%m%d%H%M%S).json
   ```

## Key Principle

**Always output to file** - This preserves the file list outside of LLM context, allowing agents to reference it later without keeping hundreds of file paths in memory.
