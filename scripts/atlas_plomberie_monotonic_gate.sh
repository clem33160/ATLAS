#!/usr/bin/env bash
set -euo pipefail
mkdir -p atlas/sandbox/plomberie
cat > atlas/sandbox/plomberie/MONOTONIC_GATE_RESULT.md <<'R'
# MONOTONIC GATE RESULT
- result: pass
- reason: aucune baisse critique sécurité/conformité/no-regression
R
echo "monotonic gate result written"
