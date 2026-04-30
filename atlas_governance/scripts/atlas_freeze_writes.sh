#!/usr/bin/env bash
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
mkdir -p atlas_governance/runtime/recovery && touch atlas_governance/runtime/recovery/LOST_MODE && echo frozen
