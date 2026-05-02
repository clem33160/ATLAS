#!/usr/bin/env bash
set -euo pipefail
if [ -z "${OPENAI_API_KEY:-}" ]; then
  echo "SKIP API eval"
  exit 0
fi
mkdir -p atlas/runtime/answers
report=atlas/reports/ATLAS_PLOMBERIE_REAL_AI_EVAL_REPORT.md
echo "# ATLAS PLOMBERIE REAL AI EVAL REPORT" > "$report"
echo "| Question | Score |" >> "$report"
echo "|---|---|" >> "$report"
for q in atlas/runtime/questions/plomberie_eval_*.md; do
  bash scripts/atlas_plomberie_ask_case.sh "$q" >/tmp/atlas_eval.log
  score=$(rg -o "SCORE=[0-9]+" /tmp/atlas_eval.log | head -n1 | cut -d= -f2)
  echo "| $(basename "$q") | ${score:-0} |" >> "$report"
done
echo "## Recommandation" >> "$report"
echo "Renforcer les rubriques manquantes sous 85/100." >> "$report"
echo "API eval done"
