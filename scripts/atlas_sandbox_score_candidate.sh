#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="$ROOT/atlas/sandbox/evolution/candidate_scorecard.md"
mkdir -p "$(dirname "$OUT")"
cat > "$OUT" <<'EOT'
# Candidate Scorecard

- sécurité: 80
- conformité: 85
- business: 78
- clarté: 82
- canon: 100
- tests: 75
- maintenabilité: 84
- total: 84
EOT
echo "scorecard written: $OUT"
