# proof1000 Sandbox

`core.proof.proof1000.run_proof1000` creates exactly 1000 fake isolated files in configured sandbox path.

Checks:
- exact file count
- every path exists
- every SHA256 matches index
- ambiguous search refusal
- delivery by `doc_id`
- apprentice access refusal
- tamper-after-index refusal

Output fields: `PASS`, `WARN`, `FAIL`, `CRITICAL_FAIL`.
Success gate: `CRITICAL_FAIL=0`.
