#!/usr/bin/env bash
set -euo pipefail
f=atlas/business/plomberie/CALL_INTAKE_PLAYBOOK.md
for k in "fuite" "gaz" "Ne jamais promettre" "résumer l'appel" "fiche CRM"; do rg -q "$k" "$f"; done
echo "call intake test OK"
