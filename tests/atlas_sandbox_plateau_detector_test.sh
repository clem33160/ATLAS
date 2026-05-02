#!/usr/bin/env bash
set -euo pipefail
bash scripts/atlas_sandbox_detect_plateau.sh || code=$?
code=${code:-0}
[ "$code" -eq 0 ] || [ "$code" -eq 2 ]
[ -f atlas/sandbox/evolution/plateau_detector.md ]
echo OK
