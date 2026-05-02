#!/usr/bin/env bash
set -euo pipefail
mkdir -p atlas/sandbox/plomberie
cat > atlas/sandbox/plomberie/PROFILE_COMPARISON_REPORT.md <<'R'
# PROFILE COMPARISON REPORT
Comparaison des profils 60/70/80/90/95/99: progression monotone visée, pas de copie des mauvaises pratiques.
R
echo "profile comparison report written"
