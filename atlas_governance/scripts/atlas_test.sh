#!/usr/bin/env bash
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
export PYTHONPATH="$(pwd):${PYTHONPATH:-}"
python -m pytest -q atlas_governance/tests
