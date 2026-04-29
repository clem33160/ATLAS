#!/usr/bin/env bash
set -euo pipefail

python3 -m atlas.main

printf "\nRapport: atlas/runtime/reports/lead_report.md\n"
echo "Export: atlas/runtime/export/leads_ranked.json"
echo "Export CSV: atlas/runtime/export/leads_ranked.csv"
echo "Résumé: atlas/runtime/outputs/run_summary.json"
