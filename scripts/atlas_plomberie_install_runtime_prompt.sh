#!/usr/bin/env bash
set -euo pipefail
target="${PREFIX:-/usr/local}/bin/atlas-plomberie-system-prompt.md"
mkdir -p "$(dirname "$target")"
cp atlas/business/plomberie/ATLAS_PLUMBING_SYSTEM_PROMPT.md "$target"
echo "prompt installed to $target"
