#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

mkdir -p \
  "$ROOT/atlas/codex_bridge/queue" \
  "$ROOT/atlas/codex_bridge/active" \
  "$ROOT/atlas/codex_bridge/reports" \
  "$ROOT/atlas/codex_bridge/accepted" \
  "$ROOT/atlas/codex_bridge/rejected" \
  "$ROOT/atlas/codex_bridge/logs" \
  "$ROOT/atlas/codex_bridge/temp" \
  "$ROOT/atlas/codex_bridge/templates" \
  "$ROOT/atlas/business/plomberie" \
  "$ROOT/atlas/sandbox/plomberie" \
  "$ROOT/atlas/reports"

chk(){ [[ -f "$1" ]] && echo "found" || echo "missing"; }
vision=$(chk "$ROOT/atlas/governance/vision/ATLAS_MASTER_VISION.md")
obj=$(chk "$ROOT/atlas/governance/vision/ATLAS_OBJECTIVE.md")
canon=$(chk "$ROOT/atlas/governance/canon/CANON_RULES.md")
qcount=$(find "$ROOT/atlas/codex_bridge/queue" -maxdepth 1 -type f -name '*.md' | wc -l | tr -d ' ')
rcount=$(find "$ROOT/atlas/codex_bridge/reports" -maxdepth 1 -type f -name '*.md' | wc -l | tr -d ' ')
status="OK"; [[ "$vision" == found && "$obj" == found && "$canon" == found ]] || status="DEGRADED"
echo "vision canonique: $vision"
echo "objectifs: $obj"
echo "règles canon: $canon"
echo "missions en queue: $qcount"
echo "rapports: $rcount"
echo "statut global Atlas Codex Bridge: $status"
