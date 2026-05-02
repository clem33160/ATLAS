#!/usr/bin/env bash
set -euo pipefail
grep -q 'Objectif' atlas/sandbox/evolution/candidate_contract.md
bash scripts/atlas_sandbox_score_candidate.sh
grep -q 'total' atlas/sandbox/evolution/candidate_scorecard.md
echo OK
