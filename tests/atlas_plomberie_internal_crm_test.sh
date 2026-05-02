#!/usr/bin/env bash
set -euo pipefail
f=atlas/business/plomberie/CRM_MODEL_PLOMBERIE.md
for k in "entrant" "qualifié" "devis envoyé" "urgence critique" "client" "adresse" "facture"; do rg -q "$k" "$f"; done
echo "internal crm test OK"
