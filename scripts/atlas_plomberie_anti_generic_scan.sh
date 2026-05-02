#!/usr/bin/env bash
set -euo pipefail
TARGETS=$(rg --files atlas/business/plomberie atlas/sandbox/plomberie atlas/governance/sandbox atlas/reports | rg "(X2|ANTI_GENERIC|CASE_BANK_200_TARGET|DETAILED_CASES_40|INNOVATION_TO_TEST_PIPELINE|NEXT_BEST_ACTION_ENGINE_SPEC)\.md$")
FAIL=0
for f in $TARGETS; do
  L=$(wc -l < "$f")
  if [ "$L" -lt 12 ]; then echo "[SHORT] $f"; FAIL=1; fi
  if rg -q "Document de renforcement|cadre opérationnel|preuves et limites" "$f"; then echo "[GENERIC] $f"; FAIL=1; fi
  if ! rg -qi "client|urgence|statut|validation|risque|test|preuve|action|cas|point" "$f"; then echo "[LACKS_CONCRETE] $f"; FAIL=1; fi
done
exit $FAIL
