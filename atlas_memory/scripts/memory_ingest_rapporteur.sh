#!/usr/bin/env bash
set -euo pipefail
ROOT=$(git rev-parse --show-toplevel)
export PYTHONPATH="$ROOT"
python - <<'PY'
from atlas_memory.src.integration import ingest_rapporteur_run
print(ingest_rapporteur_run())
PY
