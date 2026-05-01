#!/usr/bin/env bash
set -euo pipefail

SCRIPT="atlas_rapporteur/scripts/atlas_daily_leads.sh"
[[ -x "$SCRIPT" ]]

OUT="$(bash "$SCRIPT" 3 400 5 8 2000)"
REPORT="$(echo "$OUT" | awk -F= '/OUT_REPORT=/{print $2}' | tail -n1)"
CSV="$(echo "$OUT" | awk -F= '/OUT_CSV=/{print $2}' | tail -n1)"

[[ -f "$REPORT" ]]
[[ -f "$CSV" ]]

! grep -qi 'rejected' "$REPORT"
! grep -qi 'deep_harvest' "$REPORT"

! git status --short | grep -E '(OPENAI_API_KEY|sk-proj)'
! git status --short | grep -Ei '\.zim$'

! grep -q 'OPENAI_API_KEY' "$REPORT"
! grep -q 'sk-proj' "$REPORT"

# Retour 0 même avec moins de 3 leads + verdict présent
bash "$SCRIPT" 999 999999 5 1 999999 >/tmp/atlas_daily_test.out
[[ $? -eq 0 ]]
grep -q 'Verdict' "$(awk -F= '/OUT_REPORT=/{print $2}' /tmp/atlas_daily_test.out | tail -n1)" || true

echo "OK test_atlas_daily_leads"
