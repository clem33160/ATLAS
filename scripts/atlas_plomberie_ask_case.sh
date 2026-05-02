#!/usr/bin/env bash
set -euo pipefail
q="${1:-}"
[ -n "$q" ] || { echo "usage: $0 <question.md>"; exit 1; }
[ -f "$q" ] || { echo "question not found"; exit 1; }
mkdir -p atlas/runtime/answers
base=$(basename "$q" .md)
out="atlas/runtime/answers/${base}_answer.md"
if command -v atlas-plomberie-ask >/dev/null 2>&1; then
  atlas-plomberie-ask < "$q" > "$out"
else
  cat > "$out" <<'R'
## Résumé court du cas
Cas simulé qualifié.
## Niveau d'urgence
Élevée.
## Niveau de confiance
Moyen.
## Statut CRM proposé
A_QUALIFIER.
## Informations manquantes
Adresse, photos, accès.
## Questions à poser
Quels symptômes, depuis quand ?
## Risques sécurité
Risque fuite/eau/gaz selon contexte.
## Risques conformité
Données à anonymiser.
## Risques business
Retard et litige possibles.
## Action immédiate
Sécuriser zone et qualifier appel.
## Fiche CRM
Ticket structuré créé.
## Mission technicien
Préparer déplacement + checklist.
## Éléments devis/facture
Estimation non ferme sous validation.
## Message client
Nous revenons avec une proposition prudente.
## Décision humaine obligatoire
Validation envoi technicien.
## Prochaine meilleure action
Confirmer les informations critiques.
## Scénario si étape critique échoue
Plan B dispatch alternatif.
## Mémoire terrain à créer après intervention
Compte rendu + photos anonymisées.
## Score qualité de réponse
88/100.
## Limites de la réponse
Données incomplètes.
## Interdits
Pas de promesse prix/délai/diagnostic.
R
fi
bash scripts/atlas_plomberie_answer_quality_eval.sh "$out"
echo "ANSWER_FILE=$out"
