#!/usr/bin/env bash
set -euo pipefail
grep -q 'checkpoints' atlas/governance/sandbox/SANDBOX_BUDGET_GUARD.md
grep -q 'Arrêter proprement' atlas/governance/sandbox/SANDBOX_BUDGET_GUARD.md
echo OK
