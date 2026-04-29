#!/usr/bin/env bash
set -euo pipefail
MODE="${1:-run}"
python3 -m atlas.main "$MODE"
case "$MODE" in
  business) sed -n '1,120p' atlas/runtime/business/business_readiness.md ;;
  closer) sed -n '1,200p' atlas/runtime/closer/daily_call_sheet.md ;;
  crm-summary) sed -n '1,120p' atlas/runtime/crm/call_outcomes_summary.md ;;
  verbose) sed -n '1,220p' atlas/runtime/reports/lead_report.md ;;
  *) echo "Résumé généré dans atlas/runtime/" ;;
esac
