#!/usr/bin/env bash
set -euo pipefail
bash scripts/atlas_plomberie_consistency_check.sh
[[ -f atlas/sandbox/plomberie/CROSS_FILE_CONSISTENCY_RULES.md ]] || exit 1
[[ -f atlas/sandbox/plomberie/SCENARIO_COVERAGE_MATRIX.md ]] || exit 1
rg -q '0 à 100|0-100' atlas/business/plomberie/SCORING_LEADS_PLOMBERIE.md
rg -qi 'petit lead|lead moyen|gros lead|lead titan' atlas/business/plomberie/SCORING_LEADS_PLOMBERIE.md
rg -qi 'Ne jamais inventer' atlas/business/plomberie/LIMITES_CONFORMITE.md
rg -qi 'Localisation|urgence|Photos|Assurance|Accès' atlas/business/plomberie/QUESTIONS_QUALIFICATION.md
echo "atlas plomberie consistency test: OK"
