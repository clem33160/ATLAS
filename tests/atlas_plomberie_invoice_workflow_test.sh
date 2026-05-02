#!/usr/bin/env bash
set -euo pipefail
f=atlas/business/plomberie/FACTURATION_DOSSIERS.md
for k in devis facture acompte solde assurance relance; do rg -q "$k" "$f"; done
echo "invoice workflow test OK"
