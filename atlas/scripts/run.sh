#!/usr/bin/env bash
set -euo pipefail

MODE="${1:-run}"
python3 -m atlas.main "$MODE"

if [[ "$MODE" == "crm-summary" ]]; then
  echo "CRM: atlas/runtime/crm/leads_history.json"
  exit 0
fi

echo "ATLAS RAPPORTEUR D’AFFAIRES — V0.6"
echo "Status: OK"
echo "Rapport: atlas/runtime/reports/lead_report.md"
echo "Export closer: atlas/runtime/closer/daily_call_sheet.md"
echo "JSON: atlas/runtime/export/leads_ranked.json"
echo "CSV: atlas/runtime/export/leads_ranked.csv"
