#!/usr/bin/env bash
set -euo pipefail
export PYTHONPATH="$(git rev-parse --show-toplevel):${PYTHONPATH:-}"
python - <<'PY'
from pathlib import Path
from atlas_memory.src.common import read_json
from atlas_memory.src.health import compute_health
report=Path('atlas_memory/runtime/noise/quarantine_report.md')
if report.exists():
    print(report.read_text(encoding='utf-8'))
else:
    print('No quarantine report yet.')
h=compute_health(); print(h)
j=read_json(Path('atlas_memory/runtime/noise/quarantine_report.json'), {})
print('top_noise_reasons=', j.get('top_noise_reasons', []))
PY
