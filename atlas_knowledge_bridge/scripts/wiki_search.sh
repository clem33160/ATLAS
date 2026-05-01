#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOCAL_ENV="$ROOT_DIR/config/local_knowledge.env"

resolve_zim() {
  if [[ -n "${WIKI_ZIM_PATH:-}" && -f "${WIKI_ZIM_PATH}" ]]; then
    printf '%s\n' "${WIKI_ZIM_PATH}"
    return 0
  fi

  if [[ -f "$LOCAL_ENV" ]]; then
    # shellcheck disable=SC1090
    source "$LOCAL_ENV"
    if [[ -n "${WIKI_ZIM_PATH:-}" && -f "${WIKI_ZIM_PATH}" ]]; then
      printf '%s\n' "${WIKI_ZIM_PATH}"
      return 0
    fi
  fi

  local termux_primary="$HOME/atlas_knowledge/dumps/zim/wikipedia_fr_all_maxi_2026-02.zim"
  if [[ -f "$termux_primary" ]]; then
    printf '%s\n' "$termux_primary"
    return 0
  fi

  local first_glob
  first_glob="$(find "$HOME/atlas_knowledge/dumps/zim" -maxdepth 1 -type f -name '*.zim' 2>/dev/null | sort | head -n 1 || true)"
  if [[ -n "$first_glob" && -f "$first_glob" ]]; then
    printf '%s\n' "$first_glob"
    return 0
  fi

  local candidates=(
    "${ROOT_DIR}/data/wikipedia_fr.zim"
    "${ROOT_DIR}/data/wikipedia_fr_all_maxi.zim"
    "/data/wikipedia_fr.zim"
    "/data/zim/wikipedia_fr.zim"
    "$HOME/data/wikipedia_fr.zim"
  )

  local c
  for c in "${candidates[@]}"; do
    if [[ -f "$c" ]]; then
      printf '%s\n' "$c"
      return 0
    fi
  done

  return 1
}

if [[ "${1:-}" == "--print-zim" ]]; then
  resolve_zim || true
  exit 0
fi

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <query> [limit]" >&2
  echo "       $0 --print-zim" >&2
  exit 1
fi

if ! command -v kiwix-search >/dev/null 2>&1; then
  echo "ERROR: kiwix-search introuvable." >&2
  exit 2
fi

QUERY="$1"
LIMIT="${2:-20}"
ZIM_PATH="$(resolve_zim || true)"

if [[ -z "$ZIM_PATH" ]]; then
  echo "ERROR: Fichier ZIM introuvable. Définissez WIKI_ZIM_PATH ou config/local_knowledge.env." >&2
  exit 3
fi

TMP_OUT="$(mktemp)"
kiwix-search "$ZIM_PATH" "$QUERY" --limit="$LIMIT" > "$TMP_OUT"

echo "=== Recherche Wikipédia locale ==="
echo "Requête      : $QUERY"
echo "Limite       : $LIMIT"
echo "Source locale: $ZIM_PATH"
echo "---------------------------------"
cat "$TMP_OUT"
rm -f "$TMP_OUT"
