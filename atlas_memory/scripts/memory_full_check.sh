#!/usr/bin/env bash
set -euo pipefail
ROOT=$(git rev-parse --show-toplevel)
export PYTHONPATH="$ROOT"
bash atlas_memory/scripts/memory_test.sh
bash atlas_memory/scripts/memory_noise_clean.sh
bash atlas_memory/scripts/memory_anti_forgetting.sh
bash atlas_memory/scripts/memory_health.sh
bash atlas_memory/scripts/memory_doctrine_check.sh
bash atlas_memory/scripts/memory_index.sh
bash atlas_memory/scripts/memory_integrity_check.sh
