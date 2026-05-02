#!/usr/bin/env bash
set -euo pipefail
for f in ultra_sandbox_readme.md mechanism_matrix_plomberie.md test_scenarios_plomberie_v1.md adversarial_cases_plomberie.md candidate_mutation_examples.md scoring_quality_matrix.md regression_traps.md plateau_examples.md; do
  [ -f "atlas/sandbox/plomberie/$f" ]
done
echo OK
