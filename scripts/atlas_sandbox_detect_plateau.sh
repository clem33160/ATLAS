#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
LOG="$ROOT/atlas/sandbox/evolution/cycle_log.md"
OUT="$ROOT/atlas/sandbox/evolution/plateau_detector.md"
mkdir -p "$(dirname "$OUT")"
no_improve_count=$(grep -ci 'no-improvement' "$LOG" || true)
if [ "$no_improve_count" -ge 3 ]; then
  status="plateau-detected"
  code=2
else
  status="no-plateau"
  code=0
fi
cat > "$OUT" <<EOT
# Plateau Detector

- status: $status
- no_improvement_entries: $no_improve_count
- evaluated_at: $(date -u +%FT%TZ)
EOT
exit "$code"
