#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  write-feishu-markdown.sh --doc-id DOC_ID --file REPORT.md

Overwrite a Feishu doc with a local Markdown file.

Required:
  --doc-id   Feishu document id from feishu-report-manifest.json.
  --file     Local Markdown file to write.
EOF
}

DOC_ID=""
FILE=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --doc-id)
      DOC_ID="${2:-}"
      shift 2
      ;;
    --file)
      FILE="${2:-}"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
done

if [[ -z "$DOC_ID" || -z "$FILE" ]]; then
  usage >&2
  exit 1
fi

if [[ ! -f "$FILE" ]]; then
  echo "Markdown file not found: $FILE" >&2
  exit 1
fi

FIRST_LINE="$(head -n 1 "$FILE" || true)"
if [[ "$FIRST_LINE" != \#* ]]; then
  echo "Markdown file must start with a level-1 heading: $FILE" >&2
  exit 1
fi

lark-cli docs +update --api-version v2 \
  --doc "$DOC_ID" \
  --command overwrite \
  --doc-format markdown \
  --content - < "$FILE"
