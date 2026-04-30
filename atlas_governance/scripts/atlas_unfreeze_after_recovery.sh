#!/usr/bin/env bash
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
rm -f atlas_governance/runtime/recovery/LOST_MODE && echo unfrozen
