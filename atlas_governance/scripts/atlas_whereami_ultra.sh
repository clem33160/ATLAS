#!/usr/bin/env bash
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
export PYTHONPATH="$(pwd):${PYTHONPATH:-}"
python - <<'PY'
from atlas_governance.core.root_anchor import find_root
from atlas_governance.recovery.lost_mode import safe_to_modify, is_lost_mode_active
print("Root:", find_root())
print("Safe to modify:", "YES" if safe_to_modify() else "NO")
print("Lost mode:", is_lost_mode_active())
PY
