#!/usr/bin/env bash
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
python -c "from atlas_governance.recovery.self_reconstruction_engine import run; print(run())"
