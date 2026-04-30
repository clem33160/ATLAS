#!/usr/bin/env bash
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
export PYTHONPATH="$(pwd):${PYTHONPATH:-}"
python - <<'PY'
from atlas_governance.core.invariant_engine import run_invariants
from atlas_governance.recovery.boot_contract import run as boot
print({"invariants": run_invariants()["ok"], "boot": boot()["ok"]})
PY
