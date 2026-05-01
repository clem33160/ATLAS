#!/usr/bin/env bash
set -euo pipefail
ls -1t atlas_rapporteur_v1/runtime/reports/*.md 2>/dev/null | head -n1 | xargs -r cat
