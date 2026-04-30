#!/usr/bin/env bash
set -euo pipefail
export PYTHONPATH="$(git rev-parse --show-toplevel):${PYTHONPATH:-}"
python - <<'PY'
from atlas_memory.src.check_pipeline import run_memory_full_check
print(run_memory_full_check(clean_noise=True, bootstrap=True, regenerate_index=True))
PY
