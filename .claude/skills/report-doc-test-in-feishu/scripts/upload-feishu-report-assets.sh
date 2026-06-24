#!/usr/bin/env bash
set -euo pipefail

RUN_DIR=""
DEMO_DIR=""
DOC_ID=""
MIDSCENE_RUN_DIR=""
SCREENSHOT_DIR=""
SOURCE_ZIP=""
MIDSCENE_ZIP=""

media_insert_file() {
  local doc_id="$1"
  local file_path="$2"
  local media_type="$3"
  local caption="${4:-}"

  if [ ! -f "$file_path" ]; then
    echo "Media file not found: $file_path" >&2
    return 1
  fi

  local file_dir
  local file_name
  file_dir="$(cd "$(dirname "$file_path")" && pwd)"
  file_name="$(basename "$file_path")"

  if [ -n "$caption" ]; then
    (cd "$file_dir" && lark-cli docs +media-insert --doc "$doc_id" --file "./$file_name" --type "$media_type" --caption "$caption")
  else
    (cd "$file_dir" && lark-cli docs +media-insert --doc "$doc_id" --file "./$file_name" --type "$media_type")
  fi
}

zip_directory() {
  local zip_path="$1"
  local dir_path="$2"
  shift 2

  if [ ! -d "$dir_path" ]; then
    echo "Zip source directory not found: $dir_path" >&2
    return 1
  fi

  local zip_dir
  local zip_name
  local zip_abs
  local source_parent
  local source_name

  mkdir -p "$(dirname "$zip_path")"
  zip_dir="$(cd "$(dirname "$zip_path")" && pwd)"
  zip_name="$(basename "$zip_path")"
  zip_abs="$zip_dir/$zip_name"
  source_parent="$(cd "$(dirname "$dir_path")" && pwd)"
  source_name="$(basename "$dir_path")"

  rm -f "$zip_abs"
  (cd "$source_parent" && zip -r "$zip_abs" "$source_name" "$@")
}

usage() {
  cat >&2 <<'EOF'
Usage:
  upload-feishu-report-assets.sh \
    --doc-id {build_test_report_doc_id} \
    --run-dir doc-test-reports/{run-name} \
    --demo-dir doc-test-reports/{run-name}/examples/{demo-name} \
    [--midscene-run-dir {midscene_run_dir}] \
    [--screenshot-dir doc-test-reports/{run-name}/auto-test/screenshots]
EOF
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --doc-id) DOC_ID="$2"; shift 2 ;;
    --run-dir) RUN_DIR="$2"; shift 2 ;;
    --demo-dir) DEMO_DIR="$2"; shift 2 ;;
    --midscene-run-dir) MIDSCENE_RUN_DIR="$2"; shift 2 ;;
    --screenshot-dir) SCREENSHOT_DIR="$2"; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown argument: $1" >&2; usage; exit 1 ;;
  esac
done

if [ -z "$DOC_ID" ] || [ -z "$RUN_DIR" ] || [ -z "$DEMO_DIR" ]; then
  usage
  exit 1
fi

mkdir -p "$RUN_DIR"

if [ ! -d "$DEMO_DIR" ]; then
  echo "Demo directory not found: $DEMO_DIR" >&2
  exit 1
fi

demo_name="$(basename "$DEMO_DIR")"
SOURCE_ZIP="$RUN_DIR/source-${demo_name}.zip"

echo "Creating source zip: $SOURCE_ZIP"
zip_directory "$SOURCE_ZIP" "$DEMO_DIR" \
  -x "*/node_modules/*" \
  -x "*/dist/*" \
  -x "*/build/*" \
  -x "*/.gradle/*" \
  -x "*/DerivedData/*" \
  -x "*/.dart_tool/*" \
  -x "*/.git/*" \
  -x "*/.env" \
  -x "*/.env.*" \
  -x "*/local.properties" \
  -x "*/secrets.*"

echo "Uploading source zip"
media_insert_file "$DOC_ID" "$SOURCE_ZIP" file

if [ -n "$MIDSCENE_RUN_DIR" ] && [ -d "$MIDSCENE_RUN_DIR" ]; then
  MIDSCENE_ZIP="$RUN_DIR/midscene-run.zip"
  echo "Creating midscene run zip: $MIDSCENE_ZIP"
  zip_directory "$MIDSCENE_ZIP" "$MIDSCENE_RUN_DIR" \
    -x "*/.DS_Store" \
    -x "*/**/*.tmp" \
    -x "*/**/*.log.bak"
  echo "Uploading midscene run zip"
  media_insert_file "$DOC_ID" "$MIDSCENE_ZIP" file
else
  echo "Skip midscene run upload: directory not provided or not found"
fi

if [ -n "$SCREENSHOT_DIR" ] && [ -d "$SCREENSHOT_DIR" ]; then
  echo "Appending screenshot section"
  lark-cli docs +update --api-version v2 --doc "$DOC_ID" --command append \
    --doc-format markdown --content "## 自动化测试截图"

  found=0
  for img in "$SCREENSHOT_DIR"/*.png "$SCREENSHOT_DIR"/*.jpg "$SCREENSHOT_DIR"/*.jpeg; do
    [ -e "$img" ] || continue
    found=1
    filename="$(basename "$img")"
    echo "Uploading screenshot: $filename"
    media_insert_file "$DOC_ID" "$img" image "$filename"
  done
  if [ "$found" -eq 0 ]; then
    echo "No screenshot images found in $SCREENSHOT_DIR"
  fi
else
  echo "Skip screenshot upload: directory not provided or not found"
fi

echo "Asset upload completed"
