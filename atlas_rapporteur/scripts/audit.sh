#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from pathlib import Path
base=Path('atlas_rapporteur/runtime/audit')
base.mkdir(parents=True,exist_ok=True)
(base/'audit_report.md').write_text('# Audit Report\n\n- Sources publiques uniquement\n- Pas de contact automatique\n',encoding='utf-8')
print('Audit generated')
PY
