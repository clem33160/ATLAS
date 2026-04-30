#!/usr/bin/env bash
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
python - <<PY
import sys,json
from atlas_governance.core.common import repo_root,jread
r=repo_root();a=jread(r/'atlas_governance/config/atlas_authority_index.json',{})
print(a.get(sys.argv[1],'UNKNOWN'))
PY "$1"
