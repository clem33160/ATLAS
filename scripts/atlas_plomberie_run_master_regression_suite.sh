#!/usr/bin/env bash
set -euo pipefail
bash tests/atlas_plomberie_consistency_test.sh
bash tests/atlas_plomberie_monotonic_gate_test.sh
bash tests/atlas_plomberie_sandbox_guard_test.sh
echo "master regression suite: ok"
