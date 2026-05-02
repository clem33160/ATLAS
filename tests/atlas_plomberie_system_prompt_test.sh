#!/usr/bin/env bash
set -euo pipefail
f=atlas/business/plomberie/ATLAS_PLUMBING_SYSTEM_PROMPT.md
rg -q "Tu es Atlas Plomberie" "$f"
rg -q "prochaine meilleure action" "$f"
echo "system prompt test OK"
