#!/usr/bin/env bash
set -euo pipefail
MAX_CYCLES=1
DOMAIN="plomberie"
while [ "$#" -gt 0 ]; do
  case "$1" in
    --max-cycles) MAX_CYCLES="${2:-1}"; shift 2;;
    --domain) DOMAIN="${2:-plomberie}"; shift 2;;
    *) echo "unknown arg: $1"; exit 1;;
  esac
done
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
mkdir -p "$ROOT/atlas/sandbox/evolution" "$ROOT/atlas/reports"
STATE="$ROOT/atlas/sandbox/evolution/cycle_state.md"
LOG="$ROOT/atlas/sandbox/evolution/cycle_log.md"
[ -f "$STATE" ] || echo -e "# Cycle State\n- status: initialized" > "$STATE"
[ -f "$LOG" ] || echo -e "# Cycle Log (append-only)" > "$LOG"
printf '\n- %s | checkpoint | domain=%s max_cycles=%s\n' "$(date -u +%FT%TZ)" "$DOMAIN" "$MAX_CYCLES" >> "$LOG"
bash "$ROOT/scripts/atlas_sandbox_score_candidate.sh"
if bash "$ROOT/scripts/atlas_sandbox_detect_plateau.sh"; then
  echo "No plateau detected"
else
  code=$?
  if [ "$code" -eq 2 ]; then
    bash "$ROOT/scripts/atlas_sandbox_notify.sh" "Plateau detected: stop intelligent"
  else
    exit "$code"
  fi
fi
bash "$ROOT/scripts/atlas_sandbox_next_mission.sh"
echo "sandbox cycle complete"
