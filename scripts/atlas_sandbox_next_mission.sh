#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="$ROOT/atlas/sandbox/evolution/next_mission_recommendation.md"
cat > "$OUT" <<EOT
# Next Mission Recommendation

- generated_at: $(date -u +%FT%TZ)
- focus: augmenter couverture tests scénarios plomberie (10 -> 20)
- focus_2: détecteur d'incohérence inter-fichiers scoring/conformité/scénarios
- rationale: améliorer valeur prouvée sans élargir périmètre sensible
EOT
echo "next mission generated"
