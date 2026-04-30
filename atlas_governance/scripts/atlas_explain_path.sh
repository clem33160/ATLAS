#!/usr/bin/env bash
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
python -c "from atlas_governance.semantic.navigation_explainability import run; print(run())"
