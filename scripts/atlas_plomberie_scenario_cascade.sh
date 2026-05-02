#!/usr/bin/env bash
set -euo pipefail
f=atlas/sandbox/plomberie/FAILURE_CASCADE_MATRIX.md
count=$(rg -c "^\|[0-9]+\|" "$f")
echo "scenario_count=$count"
if [ "$count" -lt 20 ]; then
  echo "ERREUR: moins de 20 scénarios"
  exit 1
fi
echo "cascade scenario matrix OK"
