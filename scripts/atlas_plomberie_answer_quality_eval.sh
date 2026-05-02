#!/usr/bin/env bash
set -euo pipefail
file="${1:-}"
[ -n "$file" ] || { echo "usage: $0 <answer.md>"; exit 1; }
[ -f "$file" ] || { echo "missing answer file"; exit 1; }
missing=0
for k in "Niveau d'urgence" "Questions à poser" "Risques sécurité" "Action immédiate" "Fiche CRM" "Mission technicien" "Éléments devis/facture" "Message client" "Interdits" "Prochaine meilleure action" "Niveau de confiance" "Informations manquantes" "Décision humaine obligatoire" "Scénario" "Score qualité"; do
  if ! rg -qi "$k" "$file"; then echo "MISSING: $k"; missing=$((missing+1)); fi
done
score=$((100-missing*6))
[ $score -lt 0 ] && score=0
echo "SCORE=$score"
exit 0
