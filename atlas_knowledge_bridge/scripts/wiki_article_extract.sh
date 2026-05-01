#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <query> [limit]" >&2
  exit 1
fi

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SEARCH_SCRIPT="$ROOT_DIR/scripts/wiki_search.sh"
QUERY="$1"
LIMIT="${2:-20}"

RAW_OUTPUT="$("$SEARCH_SCRIPT" "$QUERY" "$LIMIT")"

echo "$RAW_OUTPUT" | awk -F'|' '
/^https?:\/\// {
  title=$2
  gsub(/^[ \t]+|[ \t]+$/, "", title)
  if (length(title)>0) print title
}'
