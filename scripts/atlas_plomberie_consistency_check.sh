#!/usr/bin/env bash
set -euo pipefail

req=(
  atlas/business/plomberie/SCENARIOS_PLOMBERIE.md
  atlas/business/plomberie/SCORING_LEADS_PLOMBERIE.md
  atlas/business/plomberie/LIMITES_CONFORMITE.md
  atlas/business/plomberie/QUESTIONS_QUALIFICATION.md
  atlas/sandbox/plomberie/CROSS_FILE_CONSISTENCY_RULES.md
  atlas/sandbox/plomberie/SCENARIO_COVERAGE_MATRIX.md
)
for f in "${req[@]}"; do [[ -f "$f" ]] || { echo "FAIL missing $f"; exit 1; }; done

scenarios=$(rg -c '^## [0-9]+\)' atlas/business/plomberie/SCENARIOS_PLOMBERIE.md)
(( scenarios >= 20 )) || { echo "FAIL scenarios <$scenarios> (need >=20)"; exit 1; }

for p in "gaz" "dégât des eaux" "fuite urgente" "Niveau d’urgence" "Questions à poser" "Prochaine action humaine"; do
  rg -qi "$p" atlas/business/plomberie/SCENARIOS_PLOMBERIE.md || { echo "FAIL scenario missing: $p"; exit 1; }
done

rg -q '0 à 100|0-100' atlas/business/plomberie/SCORING_LEADS_PLOMBERIE.md || { echo "FAIL scoring range"; exit 1; }
for c in "petit lead" "lead moyen" "gros lead" "lead titan"; do
  rg -qi "$c" atlas/business/plomberie/SCORING_LEADS_PLOMBERIE.md || { echo "FAIL missing category: $c"; exit 1; }
done

for p in "Ne jamais inventer prix" "Ne jamais inventer disponibilité" "Ne jamais inventer assurance" "Ne jamais inventer preuve"; do
  rg -q "$p" atlas/business/plomberie/LIMITES_CONFORMITE.md || { echo "FAIL conformité: $p"; exit 1; }
done

for p in "Localisation" "urgence" "Photos" "Assurance" "Accès"; do
  rg -qi "$p" atlas/business/plomberie/QUESTIONS_QUALIFICATION.md || { echo "FAIL qualification: $p"; exit 1; }
done

if git diff --name-only | rg -q '^atlas/governance/vision/(ATLAS_MASTER_VISION.md|ATLAS_OBJECTIVE.md)$'; then
  echo "FAIL forbidden vision file modified"
  exit 1
fi

echo "atlas plomberie consistency check: OK"
