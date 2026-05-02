#!/usr/bin/env bash
set -euo pipefail
[[ -d atlas/sandbox/plomberie ]] || exit 1
for f in regression_cases.md regression_traps.md evaluation_rules.md; do
  [[ -f "atlas/sandbox/plomberie/$f" ]] || { echo "missing $f"; exit 1; }
done
for p in "invente des données|donnée inventée" "dégrade la sécurité|sécurité" "scoring flou" "supprime une question critique" "doublon canonique" "prix certain"; do
  rg -qi "$p" atlas/sandbox/plomberie/evaluation_rules.md atlas/sandbox/plomberie/regression_traps.md || { echo "missing guard $p"; exit 1; }
done
echo "atlas plomberie sandbox guard test: OK"
