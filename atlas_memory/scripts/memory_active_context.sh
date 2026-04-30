#!/usr/bin/env bash
set -euo pipefail
ROOT=$(git rev-parse --show-toplevel)
export PYTHONPATH="$ROOT"
python - <<'PY'
from atlas_memory.src.active_context import build_active_context, save_active_context
ctx=build_active_context('memory maintenance','atlas_memory'); save_active_context(ctx); print(ctx)
PY
