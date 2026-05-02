#!/usr/bin/env bash
set -euo pipefail
f=atlas/sandbox/plomberie/SIMULATION_CASES_INTERNAL_OPERATIONS.md
n=$(rg -c '^## Case ID:' "$f")
[ "$n" -ge 50 ]
for k in appel chantier facture assurance gaz "score attendu" "action CRM attendue"; do rg -q "$k" "$f"; done
echo "simulation cases test OK ($n cases)"
