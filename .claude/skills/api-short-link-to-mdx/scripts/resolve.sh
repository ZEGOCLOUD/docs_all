#!/bin/bash
# resolve.sh — Resolve a ZEGO API short link (@xxx) to a local API reference MDX file.
#
# Usage: resolve.sh <short_link> <current_mdx_path>
#   short_link:       API name without @ (e.g., startPublishingStream, sendSEI)
#   current_mdx_path: Path of the MDX file containing the short link, relative to docs root
#
# Output (4 lines on success):
#   1. instance ID
#   2. resolved URL path (e.g., /real-time-video-web/client-sdk/api-reference/class#startpublishingstream)
#   3. local MDX file absolute path
#   4. anchor slug
#
# Exit 1 on failure with error message to stderr.

set -euo pipefail

if [ $# -lt 2 ]; then
  echo "Usage: resolve.sh <short_link> <current_mdx_path>" >&2
  exit 1
fi

SHORT_LINK="$1"
CURRENT_MDX="$2"

# Resolve docs root: walk up from this script's location to find docuo.config.json
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DOCS_ROOT=""
dir="$SCRIPT_DIR"
for _ in $(seq 1 10); do
  if [ -f "$dir/docuo.config.json" ]; then
    DOCS_ROOT="$dir"
    break
  fi
  dir="$(dirname "$dir")"
done

if [ -z "$DOCS_ROOT" ]; then
  echo "Error: Cannot find docuo.config.json from $SCRIPT_DIR" >&2
  exit 1
fi

CONFIG="$DOCS_ROOT/docuo.config.json"

# ---------- generateSlug: match the JS implementation ----------
# lowercase, remove non-word chars (except spaces and hyphens), spaces to hyphens
generate_slug() {
  echo "$1" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9 _-]//g' | sed 's/  */-/g' | sed 's/^-*//;s/-*$//'
}

# ---------- Find the instance for the current MDX file ----------
# Strategy: find the instance whose `path` is the longest prefix of CURRENT_MDX
BEST_INSTANCE_ID=""
BEST_INSTANCE_PATH=""
BEST_INSTANCE_ROUTE=""
BEST_INSTANCE_API=""
BEST_LEN=0

# Extract instances with clientApiPath using python (available everywhere)
INSTANCES=$(python3 -c "
import json, sys
with open('$CONFIG') as f:
    data = json.load(f)
for inst in data.get('instances', []):
    cap = inst.get('clientApiPath', '')
    if cap:
        print(inst.get('id',''), inst.get('path',''), inst.get('routeBasePath',''), cap)
" 2>/dev/null)

if [ -z "$INSTANCES" ]; then
  echo "Error: No instances with clientApiPath found in $CONFIG" >&2
  exit 1
fi

while IFS=' ' read -r inst_id inst_path inst_route inst_api; do
  # Check if current_mdx starts with instance path
  if [ "${CURRENT_MDX#"$inst_path"}" != "$CURRENT_MDX" ]; then
    len=${#inst_path}
    if [ "$len" -gt "$BEST_LEN" ]; then
      BEST_LEN=$len
      BEST_INSTANCE_ID=$inst_id
      BEST_INSTANCE_PATH=$inst_path
      BEST_INSTANCE_ROUTE=$inst_route
      BEST_INSTANCE_API=$inst_api
    fi
  fi
done <<< "$INSTANCES"

if [ -z "$BEST_INSTANCE_ID" ]; then
  echo "Error: No matching instance for $CURRENT_MDX" >&2
  exit 1
fi

API_DIR="$DOCS_ROOT/$BEST_INSTANCE_PATH/$BEST_INSTANCE_API"

if [ ! -d "$API_DIR" ]; then
  echo "Error: API directory not found: $API_DIR" >&2
  exit 1
fi

# ---------- Parse the short link ----------
# Heading link: starts with - (e.g., @-ZegoEngine)
# Method link: everything else
PARENT_TYPES="class interface enum protocol struct"

if [ "${SHORT_LINK:0:1}" = "-" ]; then
  LINK_TYPE="heading"
  RAW="${SHORT_LINK:1}"
else
  LINK_TYPE="method"
  RAW="$SHORT_LINK"
fi

# For heading links, check for type suffix (e.g., ZegoEngine-class)
SPECIFIED_TYPE=""
if [ "$LINK_TYPE" = "heading" ]; then
  for ptype in $PARENT_TYPES; do
    suffix="-${ptype}"
    if [ "${RAW,,}" = "${RAW%$suffix}${suffix}" ] && [ "${RAW,,}" != "${RAW%$suffix}" ]; then
      SPECIFIED_TYPE="$ptype"
      RAW="${RAW%$suffix}"
      break
    fi
  done
fi

# Generate anchor slug from the raw name
# Handle overload suffix: __1 → strip (simplified from full logic)
RAW_CLEAN="${RAW//__}"
ANCHOR=$(generate_slug "$RAW_CLEAN")

# ---------- Build URL base ----------
URL_BASE="/${BEST_INSTANCE_ROUTE}/${BEST_INSTANCE_API}"
URL_BASE=$(echo "$URL_BASE" | sed 's#/\+#/#g')

# ---------- Search for the anchor in API MDX files ----------
found_file=""
found_type=""

search_in_file() {
  local file="$1"
  local ftype="$2"
  if [ ! -f "$file" ]; then return 1; fi

  # For method links: search ParamField name= attributes
  # Normalize file content (collapse newlines) and match name="..."
  # Use grep to find lines containing name= with our anchor text
  local anchor_pattern
  anchor_pattern=$(echo "$ANCHOR" | sed 's/-/ /g')

  # Search for ParamField with name matching (case-insensitive slug match)
  # The name attr preserves original case, so search case-insensitively
  if grep -qi "name=\"${RAW_CLEAN}\"" "$file" 2>/dev/null; then
    return 0
  fi
  # Also try the original short link directly
  if grep -qi "name=\"${SHORT_LINK}\"" "$file" 2>/dev/null; then
    return 0
  fi
  # Try with overload normalization
  if [ "${RAW}" != "${RAW_CLEAN}" ] && grep -qi "name=\"${RAW_CLEAN}\"" "$file" 2>/dev/null; then
    return 0
  fi

  return 1
}

if [ "$LINK_TYPE" = "heading" ]; then
  # For heading links, search ## headings
  search_heading() {
    local file="$1"
    local ftype="$2"
    if [ ! -f "$file" ]; then return 1; fi
    # Search for headings matching the slug
    local heading_text
    heading_text=$(echo "$ANCHOR" | sed 's/-/ /g')
    if grep -qi "^##\+ .*$heading_text" "$file" 2>/dev/null; then
      return 0
    fi
    return 1
  }

  if [ -n "$SPECIFIED_TYPE" ]; then
    file="$API_DIR/${SPECIFIED_TYPE}.mdx"
    if search_heading "$file" "$SPECIFIED_TYPE"; then
      found_file="$file"
      found_type="$SPECIFIED_TYPE"
    fi
  fi

  if [ -z "$found_file" ]; then
    for ptype in $PARENT_TYPES; do
      file="$API_DIR/${ptype}.mdx"
      if search_heading "$file" "$ptype"; then
        found_file="$file"
        found_type="$ptype"
        break
      fi
    done
  fi
else
  # Method links: search ParamField in order
  if [ -n "$SPECIFIED_TYPE" ]; then
    file="$API_DIR/${SPECIFIED_TYPE}.mdx"
    if search_in_file "$file" "$SPECIFIED_TYPE"; then
      found_file="$file"
      found_type="$SPECIFIED_TYPE"
    fi
  fi

  if [ -z "$found_file" ]; then
    for ptype in $PARENT_TYPES; do
      file="$API_DIR/${ptype}.mdx"
      if search_in_file "$file" "$ptype"; then
        found_file="$file"
        found_type="$ptype"
        break
      fi
    done
  fi
fi

if [ -z "$found_file" ]; then
  echo "Error: Cannot resolve @${SHORT_LINK} in any API file under $API_DIR" >&2
  echo "  Searched anchor: ${ANCHOR}" >&2
  exit 1
fi

# ---------- Output ----------
FULL_URL="${URL_BASE}/${found_type}#${ANCHOR}"
ABS_PATH=$(cd "$(dirname "$found_file")" && pwd)/$(basename "$found_file")

echo "$BEST_INSTANCE_ID"
echo "$FULL_URL"
echo "$ABS_PATH"
echo "$ANCHOR"
