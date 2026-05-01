#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CONFIG="$ROOT_DIR/config/domain_queries.json"
EXTRACT_SCRIPT="$ROOT_DIR/scripts/wiki_article_extract.sh"
REPORT_DIR="$ROOT_DIR/runtime/reports"
mkdir -p "$REPORT_DIR"

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <plomberie|chauffage|pompe_chaleur|renovation>" >&2
  exit 1
fi

DOMAIN="$1"

if ! python3 - <<PY
import json
cfg=json.load(open('$CONFIG',encoding='utf-8'))
assert '$DOMAIN' in cfg
PY
then
  echo "ERROR: Domaine invalide: $DOMAIN" >&2
  exit 2
fi

mapfile -t QUERIES < <(python3 - <<PY
import json
cfg=json.load(open('$CONFIG',encoding='utf-8'))
for q in cfg['$DOMAIN']:
    print(q)
PY
)

TS="$(date -u +%Y%m%dT%H%M%SZ)"
REPORT_FILE="$REPORT_DIR/wiki_${DOMAIN}_${TS}.md"

{
  echo "# Pack métier: $DOMAIN"
  echo
  echo "- Généré le: $(date -u '+%Y-%m-%d %H:%M:%S UTC')"
  echo "- Source: Wikipédia locale (ZIM, via kiwix-search)"
  echo "- Preuve locale: WIKI_LOCAL_SOURCE=kiwix-search"
  echo "- Limitation: Wikipédia n'est pas une preuve commerciale."
  echo
  for q in "${QUERIES[@]}"; do
    echo "## Requête: $q"
    "$EXTRACT_SCRIPT" "$q" 15 | nl -w2 -s'. '
    echo
  done
} > "$REPORT_FILE"

echo "Pack généré: $REPORT_FILE"
