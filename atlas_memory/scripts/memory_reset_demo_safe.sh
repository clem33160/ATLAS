#!/usr/bin/env bash
set -euo pipefail
export PYTHONPATH="$(git rev-parse --show-toplevel):${PYTHONPATH:-}"
python - <<'PY'
from atlas_memory.src.common import RUNTIME_PATHS, read_jsonl, write_json
import json

raw_events = read_jsonl(RUNTIME_PATHS["raw"])
keep_raw = [e for e in raw_events if str(e.get("source", "")).lower() not in {"demo", "t", "test", "tests"}]
RUNTIME_PATHS["raw"].write_text("", encoding="utf-8")
for row in keep_raw:
    with RUNTIME_PATHS["raw"].open("a", encoding="utf-8") as h:
        h.write(json.dumps(row, ensure_ascii=False) + "\n")

semantic = read_jsonl(RUNTIME_PATHS["semantic"])
keep_sem = [s for s in semantic if s.get("source_event_id") in {e.get("event_id") for e in keep_raw}]
RUNTIME_PATHS["semantic"].write_text("", encoding="utf-8")
for row in keep_sem:
    with RUNTIME_PATHS["semantic"].open("a", encoding="utf-8") as h:
        h.write(json.dumps(row, ensure_ascii=False) + "\n")

for canon_file in RUNTIME_PATHS["canon"].glob("*.json"):
    canon = json.loads(canon_file.read_text(encoding="utf-8"))
    canon["entries"] = [e for e in canon.get("entries", []) if e.get("event_id") in {x.get("event_id") for x in keep_raw}]
    write_json(canon_file, canon)
PY
