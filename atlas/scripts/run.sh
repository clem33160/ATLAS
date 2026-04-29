#!/usr/bin/env bash
set -euo pipefail
MODE="${1:-run}"
python3 -m atlas.main "$MODE"
