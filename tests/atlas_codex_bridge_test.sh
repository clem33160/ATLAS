#!/usr/bin/env bash
set -euo pipefail
req_dirs=(atlas/codex_bridge/queue atlas/codex_bridge/active atlas/codex_bridge/reports atlas/codex_bridge/accepted atlas/codex_bridge/rejected atlas/codex_bridge/logs atlas/codex_bridge/templates)
for d in "${req_dirs[@]}"; do [[ -d "$d" ]] || { echo "Missing dir: $d"; exit 1; }; done
req_files=(atlas/codex_bridge/logs/mission_log.md scripts/atlas_create_codex_mission.sh scripts/atlas_validate_codex_mission.sh scripts/atlas_audit_codex_result.sh scripts/atlas_register_codex_result.sh scripts/atlas_print_status.sh)
for f in "${req_files[@]}"; do [[ -f "$f" ]] || { echo "Missing file: $f"; exit 1; }; done
echo "codex bridge test OK"
