#!/usr/bin/env bash
set -euo pipefail
ROOT=$(git rev-parse --show-toplevel)
export PYTHONPATH="$ROOT"
python - <<'PY'
from atlas_memory.src.doctrine_check import run_doctrine_check
r=run_doctrine_check(); print(r)
raise SystemExit(0 if r.get('doctrine_ok') else 1)
PY
