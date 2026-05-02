#!/usr/bin/env bash
set -euo pipefail
for q in atlas/runtime/questions/plomberie_eval_0{1..5}_*.md; do
  bash scripts/atlas_plomberie_ask_case.sh "$q" >/tmp/atlas_q.log
  tail -n 2 /tmp/atlas_q.log
done
echo "run_5_realistic_questions done"
