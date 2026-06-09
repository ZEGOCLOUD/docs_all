#!/usr/bin/env bash
set -euo pipefail

SPACE_ID="7187666870011232257"
PARENT_NODE_TOKEN="Bvy6wsTvjiLh7bkzOxVcwvyunTH"

RUN_DIR=""
PRODUCT=""
PLATFORM=""
SCOPE=""
DATE=""
ROLE_FILES_PATTERN=""

usage() {
  cat >&2 <<'EOF'
Usage:
  create-feishu-report-skeletons.sh \
    --run-dir doc-test-reports/{run-name} \
    --product {product} \
    --platform {platform} \
    --scope {scope} \
    --date YYYY-MM-DD \
    --role-files "doc-test-reports/{run-name}/doc-eval/role-*.md"
EOF
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --run-dir) RUN_DIR="$2"; shift 2 ;;
    --product) PRODUCT="$2"; shift 2 ;;
    --platform) PLATFORM="$2"; shift 2 ;;
    --scope) SCOPE="$2"; shift 2 ;;
    --date) DATE="$2"; shift 2 ;;
    --role-files) ROLE_FILES_PATTERN="$2"; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown argument: $1" >&2; usage; exit 1 ;;
  esac
done

if [ -z "$RUN_DIR" ] || [ -z "$PRODUCT" ] || [ -z "$PLATFORM" ] || [ -z "$SCOPE" ] || [ -z "$DATE" ]; then
  usage
  exit 1
fi

mkdir -p "$RUN_DIR"
RUN_NAME="$(basename "$RUN_DIR")"
MANIFEST="$RUN_DIR/feishu-report-manifest.json"

role_name() {
  case "$1" in
    role-cto) echo "CTO / 技术决策者" ;;
    role-support) echo "ZEGO 技术支持" ;;
    role-client-dev) echo "客户端开发" ;;
    role-server-dev) echo "服务端开发" ;;
    role-fullstack-dev) echo "全栈开发" ;;
    *) echo "$1" ;;
  esac
}

create_doc() {
  local parent_token="$1"
  local title="$2"
  lark-cli docs +create --api-version v2 \
    --parent-token "$parent_token" \
    --doc-format markdown \
    --content "$(cat <<EOF
# $title

> 报告骨架已创建，内容待写入。
EOF
)"
}

extract_json_field() {
  local json="$1"
  local field="$2"
  node -e "const fs=require('fs'); const field='$field'; const data=JSON.parse(fs.readFileSync(0,'utf8')); function find(v){ if(!v || typeof v !== 'object') return ''; if(Object.prototype.hasOwnProperty.call(v, field)) return v[field] || ''; for (const child of Object.values(v)) { const got = find(child); if (got) return got; } return ''; } console.log(find(data));" <<<"$json"
}

echo "Creating Feishu folder..."
FOLDER_TITLE="【${DATE} ${PRODUCT}-${PLATFORM}-${SCOPE} 接入测试】"
FOLDER_JSON="$(lark-cli wiki nodes create \
  --params "{\"space_id\":\"$SPACE_ID\"}" \
  --data "{\"parent_node_token\":\"$PARENT_NODE_TOKEN\",\"node_type\":\"origin\",\"obj_type\":\"docx\",\"title\":\"$FOLDER_TITLE\"}" \
  --as user)"

FOLDER_NODE_TOKEN="$(extract_json_field "$FOLDER_JSON" "node_token")"
FOLDER_URL="$(extract_json_field "$FOLDER_JSON" "url")"

if [ -z "$FOLDER_NODE_TOKEN" ]; then
  echo "Failed to parse folder node_token from lark-cli response:" >&2
  echo "$FOLDER_JSON" >&2
  exit 1
fi

tmp_manifest="$(mktemp)"
node - "$RUN_NAME" "$FOLDER_NODE_TOKEN" "$FOLDER_URL" <<'NODE' > "$tmp_manifest"
const [runName, nodeToken, url] = process.argv.slice(2);
const folder = { nodeToken, url };
const documents = {
  "build-test-report": null,
  "doc-eval-summary": null,
  "integration-summary": null,
  "doc-eval-role": {}
};
console.log(JSON.stringify({ runName, folder, documents }, null, 2));
NODE

create_and_patch_manifest() {
  local key="$1"
  local title="$2"
  local role_id="${3:-}"
  echo "Creating doc: $title"
  local response
  response="$(create_doc "$FOLDER_NODE_TOKEN" "$title")"
  local doc_id url
  doc_id="$(extract_json_field "$response" "document_id")"
  if [ -z "$doc_id" ]; then doc_id="$(extract_json_field "$response" "doc_id")"; fi
  url="$(extract_json_field "$response" "url")"
  node - "$tmp_manifest" "$key" "$role_id" "$title" "$doc_id" "$url" <<'NODE'
const fs = require("fs");
const [file, key, roleId, title, docId, url] = process.argv.slice(2);
const data = JSON.parse(fs.readFileSync(file, "utf8"));
const entry = { title, docId, url };
if (key === "doc-eval-role") data.documents[key][roleId] = entry;
else data.documents[key] = entry;
fs.writeFileSync(file, JSON.stringify(data, null, 2) + "\n");
NODE
}

create_and_patch_manifest "build-test-report" "构建与自动化测试报告"
create_and_patch_manifest "doc-eval-summary" "【文档评测报告】汇总报告"
create_and_patch_manifest "integration-summary" "接入测试综合报告"

if [ -n "$ROLE_FILES_PATTERN" ]; then
  # shellcheck disable=SC2086
  for role_file in $ROLE_FILES_PATTERN; do
    [ -e "$role_file" ] || continue
    role_id="$(basename "$role_file" .md)"
    title="【文档评测报告】$(role_name "$role_id")"
    create_and_patch_manifest "doc-eval-role" "$title" "$role_id"
  done
fi

mv "$tmp_manifest" "$MANIFEST"
echo "Wrote $MANIFEST"
