#!/usr/bin/env bash
set -euo pipefail
bash scripts/atlas_plomberie_scenario_cascade.sh
rg -q "Nœuds: A appel client" atlas/sandbox/plomberie/SCENARIO_CASCADE_ENGINE.md
rg -q "Bouclier 5" atlas/sandbox/plomberie/OPERATIONAL_RESILIENCE_MAP.md
echo "atlas plomberie scenario cascade test OK"
