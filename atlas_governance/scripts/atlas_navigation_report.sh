#!/usr/bin/env bash
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
python -c "from atlas_governance.core.invariant_engine import run_invariants;print(run_invariants())"
