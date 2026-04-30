#!/usr/bin/env bash
set -euo pipefail
export PYTHONPATH="$(git rev-parse --show-toplevel):${PYTHONPATH:-}"
python - <<'PY'
import json
from atlas_memory.src.anti_confusion import run_anti_confusion_scan
report = run_anti_confusion_scan()
print(json.dumps(report, indent=2, ensure_ascii=False))
raise SystemExit(0 if report.get('ok') else 1)
PY
