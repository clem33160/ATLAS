#!/usr/bin/env bash
set -euo pipefail
export PYTHONPATH="$(git rev-parse --show-toplevel):${PYTHONPATH:-}"
python - <<'PY'
from atlas_memory.src.check_pipeline import run_memory_full_check
r = run_memory_full_check(clean_noise=True, bootstrap=True, regenerate_index=True)
print(r)
raise SystemExit(0 if r.get('global_index_ok') and r.get('anti_forgetting_ok') else 1)
PY
