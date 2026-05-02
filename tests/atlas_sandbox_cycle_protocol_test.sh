#!/usr/bin/env bash
set -euo pipefail
for n in 1 2 3 4 5 6 7 8 9 10; do grep -q "Cycle $n" atlas/governance/sandbox/SANDBOX_CYCLE_PROTOCOL.md; done
echo OK
