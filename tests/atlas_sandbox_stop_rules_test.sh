#!/usr/bin/env bash
set -euo pipefail
grep -q 'tests échouent' atlas/governance/sandbox/SANDBOX_STOP_RULES.md
grep -q 'canon maître touché' atlas/governance/sandbox/SANDBOX_STOP_RULES.md
echo OK
