#!/usr/bin/env bash
set -euo pipefail
export PYTHONPATH="$(git rev-parse --show-toplevel):${PYTHONPATH:-}"
python - <<'PY'
import json
from atlas_memory.src.organ_score import compute_organ_score

report = compute_organ_score()
print(json.dumps(report, indent=2, ensure_ascii=False))

ok = report.get("global_organ_score", 100) < 75 and report.get("technical_health_score", 0) >= 80
raise SystemExit(0 if ok else 1)
PY
