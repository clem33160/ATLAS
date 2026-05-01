#!/usr/bin/env bash
set -euo pipefail
bash atlas_rapporteur_v1/scripts/atlas_50_leads.sh
latest=$(ls -1t atlas_rapporteur_v1/runtime/reports/report_*.md | head -n1)
test -f "$latest"
test -f "${latest%.md}.csv"
test -f "${latest%.md}.jsonl"
