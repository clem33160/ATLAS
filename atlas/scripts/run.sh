#!/usr/bin/env bash
set -euo pipefail

python3 -m atlas.main

echo "\nRapport: atlas/reports/lead_report.md"
echo "Export: atlas/export/leads_ranked.json"
