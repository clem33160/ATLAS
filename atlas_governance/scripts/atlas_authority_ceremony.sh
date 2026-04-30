#!/usr/bin/env bash
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
python -c "from atlas_governance.consensus.authority_change_ceremony import run; print(run())"
