#!/usr/bin/env bash
set -euo pipefail
BASE="$(cd "$(dirname "$0")/.." && pwd)"
D="$BASE/runtime"; TS=$(date +%Y%m%d_%H%M%S)
mkdir -p "$D"/{raw,normalized,candidates,reports,actions,audit}
RAW="$D/raw/boamp_${TS}.jsonl"; N1="$D/normalized/n1_${TS}.jsonl"; N2="$D/candidates/n2_${TS}.jsonl"; N3="$D/candidates/n3_${TS}.jsonl"; N4="$D/candidates/n4_${TS}.jsonl"; N5="$D/candidates/n5_${TS}.jsonl"; FINAL="$D/candidates/final_${TS}.jsonl"
MD="$D/reports/report_${TS}.md"; CSV="$D/reports/report_${TS}.csv"; JSONL="$D/reports/report_${TS}.jsonl"
"$BASE/connectors/boamp.sh" "$RAW"
"$BASE/connectors/place_stub.sh" > "$D/audit/place_${TS}.log"
"$BASE/connectors/ted_stub.sh" > "$D/audit/ted_${TS}.log"
"$BASE/connectors/seao_stub.sh" > "$D/audit/seao_${TS}.log"
"$BASE/connectors/canadabuys_stub.sh" > "$D/audit/canadabuys_${TS}.log"
python3 "$BASE/core/normalize.py" "$RAW" "$N1"
python3 "$BASE/core/dedupe.py" "$N1" "$N2"
python3 "$BASE/core/classify_domain.py" "$N2" "$N3" "$BASE/config/domains.json"
python3 "$BASE/core/quality_gate.py" "$N3" "$N4" "$BASE/config/compliance_policy.json"
python3 "$BASE/core/score.py" "$N4" "$N5" "$BASE/config/scoring_policy.json"
python3 "$BASE/core/commission.py" "$N5" "$FINAL"
python3 "$BASE/core/report.py" "$FINAL" "$MD" "$CSV" "$JSONL" "1" "4" "PLACE,TED,SEAO,CanadaBuys"
echo "Atlas V1 terminé: $MD"
exit 0
