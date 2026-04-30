#!/usr/bin/env bash
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
python -c "from atlas_governance.recovery.boot_contract import run; print(run())"
