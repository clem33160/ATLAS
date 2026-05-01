#!/usr/bin/env bash
set -euo pipefail
BASE="$(cd "$(dirname "$0")/.." && pwd)"
echo "Sources configured:" && cat "$BASE/config/sources.jsonl"
