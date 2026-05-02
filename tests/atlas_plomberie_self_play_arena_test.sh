#!/usr/bin/env bash
set -euo pipefail
f=atlas/sandbox/plomberie/PLUMBER_PROFILE_BENCHMARKS.md
for k in "Plombier 60" "Plombier 70" "Plombier 80" "Plombier 90" "Plombier 95" "Plombier 99" "forces" "faiblesses"; do rg -q "$k" "$f"; done
echo "self play arena test OK"
