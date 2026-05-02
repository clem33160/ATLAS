#!/usr/bin/env bash
set -euo pipefail
count=$(grep -c '^## M[0-9][0-9]' atlas/governance/sandbox/SANDBOX_MECHANISMS_70.md)
[ "$count" -ge 70 ]
grep -q 'M70' atlas/governance/sandbox/SANDBOX_MECHANISMS_70.md
echo "mechanisms=$count"
