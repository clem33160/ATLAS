#!/usr/bin/env bash
set -euo pipefail
f=atlas/sandbox/plomberie/MONOTONIC_IMPROVEMENT_GATES.md
for k in "90" "89" "sécurité" "conformité" "plateau"; do rg -q "$k" "$f"; done
echo "monotonic gate test OK"
