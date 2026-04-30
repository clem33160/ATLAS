#!/usr/bin/env bash
set -euo pipefail
export PYTHONPATH="$(git rev-parse --show-toplevel):${PYTHONPATH:-}"
python - <<'PY'
from atlas_memory.src.noise_quarantine import quarantine_noise
from atlas_memory.src.health import compute_health
r=quarantine_noise(); h=compute_health()
print(f"isolated_noise={r['quarantined_noise_count']}")
print(f"real_items_kept={r['real_items_kept']}")
print("report_path=atlas_memory/runtime/noise/quarantine_report.md")
print(f"health_memory_score={h['memory_score']}")
PY
