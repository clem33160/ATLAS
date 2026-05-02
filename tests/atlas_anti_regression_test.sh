#!/usr/bin/env bash
set -euo pipefail
[[ -f atlas/governance/safety/ANTI_REGRESSION_RULES.md ]] || { echo "Missing anti regression rules"; exit 1; }
[[ -f atlas/governance/safety/LEGAL_AND_ETHICAL_LIMITS.md ]] || { echo "Missing legal/ethical limits"; exit 1; }
[[ -f atlas/governance/safety/FORBIDDEN_ACTIONS.md ]] || { echo "Missing forbidden actions"; exit 1; }
echo "anti regression test OK"
