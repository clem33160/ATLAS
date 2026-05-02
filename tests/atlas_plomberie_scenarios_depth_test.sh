#!/usr/bin/env bash
set -euo pipefail
f=atlas/business/plomberie/SCENARIOS_PLOMBERIE.md
[[ -f "$f" ]] || { echo "missing scenarios"; exit 1; }
(( $(rg -c '^## [0-9]+\)' "$f") >= 20 )) || { echo "<20 scenarios"; exit 1; }
for p in "gaz" "dégât des eaux" "nuit/week-end" "Rénovation" "Assurance" "Niveau d’urgence" "Questions à poser" "Prochaine action humaine"; do
  rg -qi "$p" "$f" || { echo "missing $p"; exit 1; }
done
echo "atlas plomberie scenarios depth test: OK"
