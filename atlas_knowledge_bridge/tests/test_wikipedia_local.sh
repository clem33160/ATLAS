#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCRIPTS="$ROOT_DIR/scripts"
REPORT_DIR="$ROOT_DIR/runtime/reports"

pass() { echo "[PASS] $*"; }
skip() { echo "[SKIP] $*"; }
fail() { echo "[FAIL] $*"; exit 1; }

ZIM="$($SCRIPTS/wiki_search.sh --print-zim || true)"
if [[ -z "$ZIM" || ! -f "$ZIM" ]]; then
  skip "ZIM absent: tests réels Wikipedia locale ignorés"
  exit 0
fi
pass "ZIM présent: $ZIM"

command -v kiwix-search >/dev/null 2>&1 && pass "kiwix-search présent" || fail "kiwix-search absent"

count_results() {
  local q="$1"
  "$SCRIPTS/wiki_search.sh" "$q" 20 | awk '/^https?:\/\//{c++} END{print c+0}'
}

for q in "plomberie" "chauffage" "pompe chaleur"; do
  n="$(count_results "$q")"
  if [[ "$n" -ge 5 ]]; then
    pass "recherche '$q' retourne $n résultats"
  else
    fail "recherche '$q' retourne seulement $n résultats"
  fi
done

"$SCRIPTS/wiki_ingest_memory.sh" plomberie >/dev/null
LATEST="$(ls -1t "$REPORT_DIR"/wiki_plomberie_*.md | head -n 1 || true)"
[[ -n "$LATEST" && -f "$LATEST" ]] && pass "rapport généré: $LATEST" || fail "rapport non généré"

BIG_FILES="$(git -C "$ROOT_DIR/.." status --porcelain | awk '{print $2}' | xargs -r -I{} sh -c 'f="'$ROOT_DIR'/../{}"; [ -f "$f" ] && [ $(stat -c%s "$f") -gt 50000000 ] && echo {}')"
[[ -z "$BIG_FILES" ]] && pass "aucun gros fichier ajouté à Git" || fail "gros fichier détecté: $BIG_FILES"

pass "Tests Wikipédia locale terminés"
