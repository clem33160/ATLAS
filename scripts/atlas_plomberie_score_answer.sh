#!/usr/bin/env bash
set -euo pipefail
f="${1:-atlas/runtime/answers/sample_answer.md}"
if [ ! -f "$f" ]; then
  mkdir -p atlas/runtime/answers
  cp atlas/runtime/answers/plomberie_eval_01_fuite_evier_answer.md "$f" 2>/dev/null || echo "## Prochaine meilleure action" > "$f"
fi
bash scripts/atlas_plomberie_answer_quality_eval.sh "$f"
for bad in "prix ferme" "délai certain" "diagnostic définitif"; do
  if rg -qi "$bad" "$f"; then echo "AUTO_REFUS: $bad"; exit 2; fi
done
echo "score answer done"
