#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
MSG="${1:-Sandbox alert}"
STATE="$ROOT/atlas/sandbox/evolution/cycle_state.md"
LOG="$ROOT/atlas/sandbox/evolution/cycle_log.md"
ALERT="$ROOT/atlas/sandbox/evolution/ALERT_CURRENT.md"
REPORT_ALERT="$ROOT/atlas/reports/ALERT_SANDBOX.md"
mkdir -p "$(dirname "$STATE")" "$ROOT/atlas/reports"
echo "# ALERT CURRENT

$MSG" > "$ALERT"
printf '\n- %s | alert | %s\n' "$(date -u +%FT%TZ)" "$MSG" >> "$LOG"
echo "- alert: $MSG" >> "$STATE"
echo "# Sandbox Alert

$MSG" > "$REPORT_ALERT"
echo "[ATLAS SANDBOX ALERT] $MSG"
if command -v termux-notification >/dev/null 2>&1; then
  termux-notification --title "ATLAS Sandbox" --content "$MSG" || true
fi
