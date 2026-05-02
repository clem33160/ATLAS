#!/usr/bin/env bash
set -euo pipefail
q=atlas/runtime/questions/plomberie_eval_01_fuite_evier.md
bash scripts/atlas_plomberie_ask_case.sh "$q" | rg -q "ANSWER_FILE="
rg -q "Prochaine meilleure action" atlas/runtime/answers/plomberie_eval_01_fuite_evier_answer.md
echo "ask case test OK"
