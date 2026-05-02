#!/usr/bin/env bash
set -euo pipefail
f=atlas/sandbox/plomberie/DYNAMIC_CANDIDATE_SCORING.md
for k in "0-100" "seuil acceptation" "seuil refus" "no-regression confidence"; do rg -q "$k" "$f"; done
echo "dynamic scoring test OK"
