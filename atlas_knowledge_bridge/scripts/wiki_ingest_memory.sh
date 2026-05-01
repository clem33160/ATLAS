#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DOMAIN_SCRIPT="$ROOT_DIR/scripts/wiki_domain_pack.sh"
REPORT_DIR="$ROOT_DIR/runtime/reports"

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <plomberie|chauffage|pompe_chaleur|renovation>" >&2
  exit 1
fi

DOMAIN="$1"
OUT="$("$DOMAIN_SCRIPT" "$DOMAIN")"
printf '%s\n' "$OUT"
LATEST="$(ls -1t "$REPORT_DIR"/wiki_${DOMAIN}_*.md | head -n 1)"

echo "=== Résumé d'ingestion Atlas ==="
echo "Report: $LATEST"
echo "Statut: disponible pour consultation locale"
echo "Rappel: Wikipédia locale = base documentaire, pas preuve commerciale."
