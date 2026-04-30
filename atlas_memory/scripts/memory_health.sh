#!/usr/bin/env bash
set -euo pipefail
export PYTHONPATH="$(git rev-parse --show-toplevel):${PYTHONPATH:-}"
python -m atlas_memory.src.main health
