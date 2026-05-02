#!/usr/bin/env bash
set -euo pipefail
bash scripts/atlas_plomberie_score_answer.sh atlas/runtime/answers/plomberie_eval_01_fuite_evier_answer.md | rg -q "score answer done"
echo "score answer test OK"
