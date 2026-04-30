#!/usr/bin/env bash
set -euo pipefail
export PYTHONPATH="$(git rev-parse --show-toplevel):${PYTHONPATH:-}"
python -m atlas_memory.src.main ingest --kind "${1:-conversation}" --domain "${2:-rapporteur_affaires}" --content "${3:-client cherche plombier Lyon fuite urgente}"
