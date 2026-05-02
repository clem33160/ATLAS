#!/usr/bin/env bash
set -euo pipefail
mkdir -p atlas/sandbox/evolution
cat > atlas/sandbox/evolution/next_mission_recommendation.md <<'R'
# Next Mission Recommendation
- intégrer retours terrain réels anonymisés
- calibrer scoring avec données de vrais dossiers
- créer moteur de priorisation intervention
- créer moteur de relance intelligente
- créer méta-sandbox qui teste les tests plomberie
- créer benchmark 100 cas internes
- créer comparateur facture/devis/chantier
R
echo "next mission written"
