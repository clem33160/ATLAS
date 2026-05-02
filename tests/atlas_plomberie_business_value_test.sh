#!/usr/bin/env bash
set -euo pipefail
rg -qi 'Qualification.*Scoring.*Action humaine|Action humaine' atlas/business/plomberie/WORKFLOW_CLIENT_PLOMBERIE.md
rg -qi 'relance|conversion|suivi' atlas/business/plomberie/WORKFLOW_CLIENT_PLOMBERIE.md
rg -qi 'valeur potentielle|business' atlas/business/plomberie/SCORING_LEADS_PLOMBERIE.md
rg -qi 'RAPPORT MODELE|rapport' atlas/business/plomberie/RAPPORT_MODELE_PLOMBERIE.md
! rg -qi 'promesse.*automatique.*dangereuse|garantie certaine automatique' atlas/business/plomberie/WORKFLOW_CLIENT_PLOMBERIE.md
echo "atlas plomberie business value test: OK"
