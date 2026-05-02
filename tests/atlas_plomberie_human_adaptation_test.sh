#!/usr/bin/env bash
set -euo pipefail
rg -q "messages incomplets" atlas/business/plomberie/HUMAN_LANGUAGE_ADAPTATION.md
rg -q "Rôles supportés" atlas/business/plomberie/USER_ROLE_ADAPTATION.md
rg -q "pas de promesse de prix ferme" atlas/business/plomberie/CLIENT_COMMUNICATION_MODES.md
echo "atlas plomberie human adaptation test OK"
