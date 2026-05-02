#!/usr/bin/env bash
set -euo pipefail
test -x scripts/atlas_plomberie_generate_missing_tests.sh
bash scripts/atlas_plomberie_generate_missing_tests.sh >/dev/null
f=atlas/sandbox/plomberie/MISSING_TESTS_REPORT.md
for k in "tests existants" "tests manquants" "prochaine mission"; do rg -q "$k" "$f"; done
echo "missing tests generator test OK"
