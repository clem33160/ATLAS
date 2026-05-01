#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SEARCH_SCRIPT="$ROOT_DIR/scripts/wiki_search.sh"

pass() { echo "[OK] $*"; }
warn() { echo "[WARN] $*"; }
fail() { echo "[FAIL] $*"; }

ZIM_PATH="$($SEARCH_SCRIPT --print-zim || true)"

echo "=== Wiki Doctor Atlas ==="
echo "Date UTC : $(date -u '+%Y-%m-%d %H:%M:%S UTC')"

if [[ -n "$ZIM_PATH" && -f "$ZIM_PATH" ]]; then
  SIZE="$(stat -c%s "$ZIM_PATH" 2>/dev/null || echo 0)"
  pass "ZIM détecté: $ZIM_PATH"
  pass "Taille (octets): $SIZE"
else
  warn "ZIM non détecté"
fi

if command -v kiwix-search >/dev/null 2>&1; then
  pass "kiwix-search disponible"
else
  fail "kiwix-search indisponible"
fi

if command -v kiwix-serve >/dev/null 2>&1; then
  pass "kiwix-serve disponible"
else
  warn "kiwix-serve indisponible"
fi

OVERALL=0
if [[ -z "$ZIM_PATH" || ! -f "$ZIM_PATH" ]]; then
  OVERALL=1
else
  for q in "plomberie" "chauffage" "pompe chaleur"; do
    n="$($SEARCH_SCRIPT "$q" 10 | awk '/^https?:\/\//{c++} END{print c+0}')"
    if [[ "$n" -ge 1 ]]; then
      pass "Recherche '$q': $n résultats"
    else
      fail "Recherche '$q': 0 résultat"
      OVERALL=1
    fi
  done
fi

if [[ "$OVERALL" -eq 0 ]]; then
  echo "STATUT: OK"
  exit 0
fi

echo "STATUT: FAIL"
exit 1
