#!/usr/bin/env bash
set -euo pipefail
export PYTHONPATH="$(git rev-parse --show-toplevel):${PYTHONPATH:-}"
python -m atlas_memory.src.main promote-canon --domain "$1" --event-id "$2" --reason "${3:-validated memory}"
