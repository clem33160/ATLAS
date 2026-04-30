#!/usr/bin/env bash
set -euo pipefail
python3 -m atlas_rapporteur.src.main --dry-run >/dev/null 2>&1 || true
python3 - <<'PY'
from atlas_rapporteur.src.db import init_db
init_db()
print('DB initialized')
PY
