#!/usr/bin/env bash
set -euo pipefail
[[ -f 'atlas/sandbox/plomberie/INTERNAL_OPERATIONS_CASE_BANK.md' ]]
count=$(rg -c '^## CASE-' atlas/sandbox/plomberie/INTERNAL_OPERATIONS_CASE_BANK.md); [[ $count -ge 100 ]]
echo 'atlas_plomberie_internal_cases_bank_test.sh OK'
