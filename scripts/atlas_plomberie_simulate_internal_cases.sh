#!/usr/bin/env bash
set -euo pipefail
mkdir -p atlas/sandbox/plomberie
cases=$(rg -c '^## Case ID:' atlas/sandbox/plomberie/SIMULATION_CASES_INTERNAL_OPERATIONS.md)
cat > atlas/sandbox/plomberie/SIMULATION_RUN_REPORT.md <<R
# SIMULATION RUN REPORT
- cases_detected: $cases
- status: simulated
- decision: candidate
R
echo "simulation report written"
