#!/usr/bin/env bash
set -euo pipefail
MAX_CYCLES=1
DOMAIN=""
DRY_RUN=0
STOP_ON_PLATEAU=0
STOP_ON_RISK=0
WRITE_NEXT=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    --max-cycles) MAX_CYCLES="$2"; shift 2;;
    --domain) DOMAIN="$2"; shift 2;;
    --dry-run) DRY_RUN=1; shift;;
    --stop-on-plateau) STOP_ON_PLATEAU=1; shift;;
    --stop-on-risk) STOP_ON_RISK=1; shift;;
    --write-next-mission) WRITE_NEXT=1; shift;;
    *) echo "unknown arg: $1"; exit 1;;
  esac
done
[[ "$DOMAIN" == "plomberie" ]] || { echo "domain must be plomberie"; exit 1; }
mkdir -p atlas/sandbox/evolution atlas/codex_bridge/queue
LOG="atlas/sandbox/evolution/plomberie_cycle_log.md"
echo "# Plomberie Autopilot Cycle Log" > "$LOG"
for ((c=1;c<=MAX_CYCLES;c++)); do
  echo "- cycle $c domain=$DOMAIN dry_run=$DRY_RUN" >> "$LOG"
  bash scripts/atlas_plomberie_consistency_check.sh >> "$LOG"
  bash scripts/atlas_plomberie_monotonic_gate.sh >> "$LOG"
  [[ $STOP_ON_PLATEAU -eq 1 ]] && echo "- stop_on_plateau: enabled" >> "$LOG"
  [[ $STOP_ON_RISK -eq 1 ]] && echo "- stop_on_risk: enabled" >> "$LOG"
  [[ $DRY_RUN -eq 1 ]] && break
done
if [[ $WRITE_NEXT -eq 1 ]]; then
  bash scripts/atlas_plomberie_generate_codex_mission.sh
fi
echo "autopilot cycle done"
