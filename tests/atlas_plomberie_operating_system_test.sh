#!/usr/bin/env bash
set -euo pipefail
for f in PLUMBING_OPERATING_SYSTEM CRM_MODEL_PLOMBERIE CALL_INTAKE_PLAYBOOK CHANTIER_WORKFLOW FACTURATION_DOSSIERS INTERVENTION_MEMORY KPIS_PLOMBERIE; do test -f "atlas/business/plomberie/${f}.md"; done
echo "operating system test OK"
