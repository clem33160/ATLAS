#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
echo "== ATLAS SANDBOX REPORT =="
for f in \
  atlas/sandbox/evolution/cycle_state.md \
  atlas/sandbox/evolution/cycle_log.md \
  atlas/sandbox/evolution/plateau_detector.md \
  atlas/sandbox/evolution/next_mission_recommendation.md \
  atlas/sandbox/evolution/ALERT_CURRENT.md \
  atlas/sandbox/plomberie/ultra_sandbox_readme.md; do
  p="$ROOT/$f"
  if [ -f "$p" ]; then
    echo "---- $f"; tail -n 20 "$p"
  fi
done
