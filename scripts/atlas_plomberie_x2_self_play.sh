#!/usr/bin/env bash
set -euo pipefail
FILE=atlas/sandbox/plomberie/PLUMBER_PROFILE_LIBRARY_X2.md
COUNT=$(rg -c "^- Cas" "$FILE")
echo "Profiles listed: $COUNT"
[ "$COUNT" -ge 12 ]
