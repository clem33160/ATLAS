#!/usr/bin/env bash
set -euo pipefail
ID="${1:-}"; STATUS="${2:-}"; SUMMARY="${3:-}"
[[ -n "$ID" && -n "$STATUS" && -n "$SUMMARY" ]] || { echo "Usage: $0 <mission-id> <status> <summary>"; exit 1; }
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RDIR="$ROOT/atlas/codex_bridge/reports"; LFILE="$ROOT/atlas/codex_bridge/logs/mission_log.md"
mkdir -p "$RDIR"
RFILE="$RDIR/${ID}_report.md"
[[ -f "$RFILE" ]] && { echo "Report already exists"; exit 1; }
cat > "$RFILE" <<MD
# Codex Result Report
- Mission ID: $ID
- Status: $STATUS
- Summary: $SUMMARY
- Timestamp (UTC): $(date -u +%Y-%m-%dT%H:%M:%SZ)
MD
echo "- $(date -u +%Y-%m-%dT%H:%M:%SZ) | $ID | $STATUS | $SUMMARY" >> "$LFILE"
echo "$RFILE"
