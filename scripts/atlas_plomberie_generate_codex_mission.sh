#!/usr/bin/env bash
set -euo pipefail
mkdir -p atlas/codex_bridge/queue
TS=$(date -u +%Y%m%dT%H%M%SZ)
OUT="atlas/codex_bridge/queue/MISSION-$TS.md"
cat > "$OUT" <<EOF
# Mission Codex Plomberie
- objectif: combler tests manquants critiques et renforcer sécurité/conformité
- chemins autorisés: atlas/business/plomberie/, atlas/sandbox/plomberie/, scripts/, tests/
- chemins interdits: atlas/governance/vision/ATLAS_MASTER_VISION.md, atlas/governance/vision/ATLAS_OBJECTIVE.md
- tests: governance, plomberie, sandbox, monotonic gate
- critères acceptation: zéro régression, sécurité >= 90, conformité >= 90
- validation humaine: obligatoire avant merge
EOF
echo "generated: $OUT"
