#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

required=(
  "atlas/business/plomberie/README.md"
  "atlas/business/plomberie/CANON_PLOMBERIE.md"
  "atlas/business/plomberie/VOCABULAIRE_PLOMBERIE.md"
  "atlas/business/plomberie/SCENARIOS_PLOMBERIE.md"
  "atlas/business/plomberie/QUESTIONS_QUALIFICATION.md"
  "atlas/business/plomberie/SCORING_LEADS_PLOMBERIE.md"
  "atlas/business/plomberie/LIMITES_CONFORMITE.md"
  "atlas/business/plomberie/WORKFLOW_CLIENT_PLOMBERIE.md"
  "atlas/business/plomberie/RAPPORT_MODELE_PLOMBERIE.md"
  "atlas/sandbox/plomberie/README.md"
  "atlas/sandbox/plomberie/candidate_input_example.md"
  "atlas/sandbox/plomberie/evaluation_rules.md"
  "atlas/sandbox/plomberie/regression_cases.md"
)

for f in "${required[@]}"; do
  [[ -f "$ROOT/$f" ]] || { echo "missing: $f"; exit 1; }
done

rg -q "## 10\)" "$ROOT/atlas/business/plomberie/SCENARIOS_PLOMBERIE.md"
rg -q "0 à 100" "$ROOT/atlas/business/plomberie/SCORING_LEADS_PLOMBERIE.md"
rg -q "Ne pas inventer de client" "$ROOT/atlas/business/plomberie/LIMITES_CONFORMITE.md"

if rg -n "final|final_final|v2|new|nouveau|patch" "$ROOT/atlas/business/plomberie" "$ROOT/atlas/sandbox/plomberie"; then
  echo "forbidden naming found"
  exit 1
fi

git -C "$ROOT" diff --quiet -- atlas/governance/vision/ATLAS_MASTER_VISION.md
git -C "$ROOT" diff --quiet -- atlas/governance/vision/ATLAS_OBJECTIVE.md

echo "atlas plomberie pack test: ok"
