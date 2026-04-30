#!/usr/bin/env bash
set -euo pipefail
export PYTHONPATH="$(git rev-parse --show-toplevel):${PYTHONPATH:-}"
python - <<'PY'
import json
from pathlib import Path
from atlas_memory.src.common import RUNTIME_PATHS, read_json, read_jsonl, write_json


def contains_marker(value):
    t = str(value).lower()
    return any(m in t for m in ("demo", "test", "synthetic", "cmd_demo"))


def is_demo_like(item):
    if contains_marker(item.get("source", "")) or contains_marker(item.get("domain", "")):
        return True
    if "client cherche plombier lyon fuite urgente" in str(item.get("content", "")).lower():
        return True
    for tag in item.get("tags", []) or []:
        if contains_marker(tag):
            return True
    if contains_marker(item.get("metadata", {})):
        return True
    return contains_marker(item)


raw = read_jsonl(RUNTIME_PATHS["raw"])
removed_event_ids = {e.get("event_id") for e in raw if is_demo_like(e)}
keep_raw = [e for e in raw if e.get("event_id") not in removed_event_ids]
RUNTIME_PATHS["raw"].write_text("", encoding="utf-8")
with RUNTIME_PATHS["raw"].open("a", encoding="utf-8") as h:
    for row in keep_raw:
        h.write(json.dumps(row, ensure_ascii=False) + "\n")

for key in ["semantic", "conflict", "uncertainty", "audit", "objectives", "procedures", "temporal", "simulation"]:
    path = RUNTIME_PATHS[key]
    rows = read_jsonl(path)
    kept = []
    for row in rows:
        row_text = json.dumps(row, ensure_ascii=False).lower()
        if any(eid and eid in row_text for eid in removed_event_ids):
            continue
        if is_demo_like(row):
            continue
        kept.append(row)
    path.write_text("", encoding="utf-8")
    with path.open("a", encoding="utf-8") as h:
        for row in kept:
            h.write(json.dumps(row, ensure_ascii=False) + "\n")

for canon_file in RUNTIME_PATHS["canon"].glob("*.json"):
    canon = read_json(canon_file, {})
    entries = canon.get("entries", [])
    canon["entries"] = [e for e in entries if e.get("event_id") not in removed_event_ids and not is_demo_like(e)]
    if contains_marker(canon.get("domain", "")):
        canon["entries"] = []
    write_json(canon_file, canon)

active = read_json(RUNTIME_PATHS["active"], {})
if is_demo_like(active):
    write_json(RUNTIME_PATHS["active"], {})
PY
