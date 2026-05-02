#!/usr/bin/env bash
set -euo pipefail
bash scripts/atlas_sandbox_next_mission.sh
grep -q 'focus' atlas/sandbox/evolution/next_mission_recommendation.md
echo OK
