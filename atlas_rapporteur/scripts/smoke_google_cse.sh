#!/usr/bin/env bash
set -euo pipefail

# Ultra-limited real API smoke test: 5 queries max by default.
LIMIT="${1:-5}"
PYTHONPATH=. python3 -m atlas_rapporteur.src.main --mode google-cse --limit "${LIMIT}"
