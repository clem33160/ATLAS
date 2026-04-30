#!/usr/bin/env bash
set -euo pipefail
MODE="${1:-dry-run}"
export PYTHONPATH="$(git rev-parse --show-toplevel):${PYTHONPATH:-}"
python - <<PY
import json
from atlas_memory.src.production_readiness import run_production_check
report = run_production_check(mode='${MODE}')
print(json.dumps(report, indent=2, ensure_ascii=False))
raise SystemExit(0 if report.get('ok') else 1)
PY
