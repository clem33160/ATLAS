#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
req_files=(
"atlas/AGENTS.md"
"atlas/governance/vision/ATLAS_MASTER_VISION.md"
"atlas/governance/missions/MISSION_CONTRACT.md"
"atlas/reports/ATLAS_VISION_IMPLANTATION_REPORT.md"
"atlas/codex_bridge/logs/mission_log.md"
"tests/atlas_governance_test.sh"
)
for f in "${req_files[@]}"; do [[ -f "$ROOT/$f" ]] || { echo "Missing required file: $f"; exit 1; }; done
bad=$(find "$ROOT" -type f | grep -E '/(final|final_final|v2|new|nouveau|patch)(\.|$)' || true)
[[ -z "$bad" ]] || { echo "Forbidden file names detected"; echo "$bad"; exit 1; }
for m in "$ROOT"/atlas/codex_bridge/queue/*.md; do [[ -e "$m" ]] || break; "$ROOT/scripts/atlas_validate_codex_mission.sh" "$m" >/dev/null; done
echo "Audit OK"
