#!/usr/bin/env bash
set -euo pipefail

python3 -m atlas.main

printf "\nRapport: atlas/reports/lead_report.md\n"
echo "Export: atlas/export/leads_ranked.json"
echo "Export CSV: atlas/export/leads_ranked.csv"
