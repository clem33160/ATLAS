#!/usr/bin/env bash
set -euo pipefail
mkdir -p atlas/sandbox/plomberie
existing=$(rg --files tests | wc -l | tr -d ' ')
cat > atlas/sandbox/plomberie/MISSING_TESTS_REPORT.md <<R
# MISSING TESTS REPORT
- tests existants: $existing
- tests manquants: couverture fine KPI, litiges, dossiers assurance multi-étapes
- priorité: haute sur sécurité/conformité, moyenne sur performance
- prochaine mission Codex recommandée: ajouter tests de granularité scoring par sous-dimension
R
echo "missing tests report written"
