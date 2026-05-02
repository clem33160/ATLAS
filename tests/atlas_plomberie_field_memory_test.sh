#!/usr/bin/env bash
set -euo pipefail
f=atlas/business/plomberie/INTERVENTION_MEMORY.md
for k in "cause probable" "cause confirmée" "action réalisée" "matériel" "durée" "leçon"; do rg -q "$k" "$f"; done
echo "field memory test OK"
