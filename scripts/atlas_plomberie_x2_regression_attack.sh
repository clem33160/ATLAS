#!/usr/bin/env bash
set -euo pipefail
FILE=atlas/sandbox/plomberie/REGRESSION_ATTACK_CASES.md
COUNT=$(rg -c "^- Cas" "$FILE")
echo "Regression cases: $COUNT"
[ "$COUNT" -ge 25 ]
