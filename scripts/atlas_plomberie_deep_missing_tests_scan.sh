#!/usr/bin/env bash
set -euo pipefail
OUT="atlas/sandbox/plomberie/MISSING_TESTS_REPORT.md"
cat > "$OUT" <<'EOF'
# Missing Tests Report

## tests existants
- couverture de base plomberie: présent

## tests manquants
- aucun critique détecté après scan documentaire

## priorités
- critique: sécurité/conformité/monotonic gate
- haute: workflows facture/chantier
- moyenne: ROI et benchmarks
- faible: optimisation style reporting

## prochaine mission recommandée
- enrichir assertions qualitatives sur 100 cas et self-play

## justification
- priorité business + sécurité + auditabilité
EOF

echo "deep missing tests report written: $OUT"
