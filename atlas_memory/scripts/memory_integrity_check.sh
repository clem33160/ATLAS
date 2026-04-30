#!/usr/bin/env bash
set -euo pipefail
ROOT=$(git rev-parse --show-toplevel)
export PYTHONPATH="$ROOT"
python - <<'PY'
from atlas_memory.src.integrity_check import run_integrity_check
r=run_integrity_check(); print(r)
raise SystemExit(0 if r.get('global_index_ok') else 1)
PY
