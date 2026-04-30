#!/usr/bin/env bash
set -euo pipefail
export PYTHONPATH="$(git rev-parse --show-toplevel):${PYTHONPATH:-}"
python - <<'PY'
import json
from atlas_memory.src.check_pipeline import run_memory_full_check

report = run_memory_full_check(clean_noise=True, bootstrap=True, regenerate_index=True)
print(json.dumps(report, indent=2, ensure_ascii=False))

ok = (
    report.get("anti_forgetting_ok") is True
    and report.get("global_index_ok") is True
    and report.get("memory_score", 0) >= 100
)
raise SystemExit(0 if ok else 1)
PY
