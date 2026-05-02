#!/usr/bin/env bash
set -euo pipefail
rg -n "^#|^##|ID|urgence" atlas/sandbox/plomberie/INTERNAL_OPERATIONS_CASE_BANK.md >/dev/null
echo "case bank audit: ok"
