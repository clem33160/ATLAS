#!/usr/bin/env bash
set -euo pipefail
./atlas/scripts/source_audit.sh
./atlas/scripts/test.sh
./atlas/scripts/run.sh
./atlas/scripts/run.sh business
./atlas/scripts/run.sh closer
test -f atlas/runtime/reports/lead_report.md
test -f atlas/runtime/closer/daily_call_sheet.md
sed -n '1,80p' atlas/runtime/business/business_readiness.md
