#!/usr/bin/env bash
set -euo pipefail
bad=$(find . -type f | grep -E '/(final|final_final|v2|new|nouveau|patch)(\.|$)' || true)
[[ -z "$bad" ]] || { echo "Forbidden names found"; echo "$bad"; exit 1; }
[[ -f atlas/reports/ATLAS_VISION_IMPLANTATION_REPORT.md ]] || { echo "Missing implantation report"; exit 1; }
echo "no chaos test OK"
