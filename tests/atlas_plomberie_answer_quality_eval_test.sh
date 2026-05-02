#!/usr/bin/env bash
set -euo pipefail
tmp=$(mktemp)
cat > "$tmp" <<'R'
Niveau d'urgence
Questions à poser
Risques sécurité
Action immédiate
Fiche CRM
Mission technicien
Éléments devis/facture
Message client
Interdits
Prochaine meilleure action
Niveau de confiance
Informations manquantes
Décision humaine obligatoire
Scénario
Score qualité
R
bash scripts/atlas_plomberie_answer_quality_eval.sh "$tmp" | rg -q "SCORE="
echo "answer quality eval test OK"
