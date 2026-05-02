#!/usr/bin/env bash
set -euo pipefail
bash scripts/atlas_sandbox_notify.sh "test notification"
[ -f atlas/sandbox/evolution/ALERT_CURRENT.md ]
grep -q 'test notification' atlas/sandbox/evolution/ALERT_CURRENT.md
echo OK
