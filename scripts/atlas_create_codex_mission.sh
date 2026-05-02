#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
QUEUE_DIR="$ROOT/atlas/codex_bridge/queue"
mkdir -p "$QUEUE_DIR"

TYPE=""; DOMAIN=""; OBJECTIVE=""; ALLOWED=""; FORBIDDEN=""; TESTS=""; VALIDATION=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --type) TYPE="${2:-}"; shift 2 ;;
    --domain) DOMAIN="${2:-}"; shift 2 ;;
    --objective) OBJECTIVE="${2:-}"; shift 2 ;;
    --allowed-paths) ALLOWED="${2:-}"; shift 2 ;;
    --forbidden-paths) FORBIDDEN="${2:-}"; shift 2 ;;
    --tests) TESTS="${2:-}"; shift 2 ;;
    --validation-level) VALIDATION="${2:-}"; shift 2 ;;
    *) echo "Unknown arg: $1"; exit 1 ;;
  esac
done

[[ -n "$TYPE" && -n "$DOMAIN" && -n "$OBJECTIVE" && -n "$ALLOWED" && -n "$FORBIDDEN" && -n "$TESTS" && -n "$VALIDATION" ]] || { echo "Missing required arguments"; exit 1; }

TS="$(date -u +%Y%m%d-%H%M%S)"
ID="MISSION-${TS}-$(printf '%03d' $((RANDOM%1000)))"
OUT="$QUEUE_DIR/${ID}.md"

cat > "$OUT" <<MD
# Codex Mission

- Mission ID: $ID
- Objectif: $OBJECTIVE
- Domaine: $DOMAIN
- Type: $TYPE
- Contexte: Mission générée automatiquement par atlas_create_codex_mission.sh
- Chemins autorisés: $ALLOWED
- Chemins interdits: $FORBIDDEN
- Fichiers à ne jamais toucher: atlas/governance/vision/ATLAS_MASTER_VISION.md
- Règles obligatoires: Respect AGENTS.md, MISSION_CONTRACT.md, tests obligatoires
- Tests obligatoires: $TESTS
- Critères d’acceptation: Livrable conforme, tests passants, aucun changement hors périmètre
- Critères de refus: Échec tests, violation sécurité/canon, manque de rapport
- Rapport final attendu: Rapport Markdown détaillant changements, tests, limites
- Niveau de validation humaine requis: $VALIDATION
MD

echo "$OUT"
