#!/usr/bin/env bash
set -euo pipefail
ROOT=$(git rev-parse --show-toplevel)
export PYTHONPATH="$ROOT"
python - <<'PY'
from atlas_memory.src.global_index import generate_global_index
print(generate_global_index())
PY
