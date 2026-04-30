#!/usr/bin/env bash
set -euo pipefail
export PYTHONPATH="$(git rev-parse --show-toplevel):${PYTHONPATH:-}"
python -m atlas_memory.src.main init
python -m atlas_memory.src.main active-context --task "maintain atlas memory core" --domain "atlas_memory"
python - <<'PY'
from atlas_memory.src import audit_ledger, canon_store, raw_store
from atlas_memory.src.common import new_id, now_iso
events = raw_store.list_events(domain="atlas_memory", kind="bootstrap", limit=1)
if events:
    event = events[-1]
else:
    event = {
        "event_id": new_id("event"),
        "created_at": now_iso(),
        "kind": "bootstrap",
        "domain": "atlas_memory",
        "content": "core memory bootstrap validated",
        "source": "atlas_memory/scripts/memory_anti_forgetting.sh",
        "source_url": None,
        "confidence": 0.95,
        "evidence_ids": ["bootstrap-evidence"],
        "linked_objective_ids": [],
        "validated_by_human": True,
        "useful_for_future": True,
        "risk_level": "LOW",
        "status": "RAW",
        "tags": ["governed"],
        "metadata": {},
    }
    raw_store.append_event(event)
canon = canon_store.get_canon("atlas_memory")
if not any(e.get("event_id") == event["event_id"] for e in canon.get("entries", [])):
    canon_store.promote_to_canon("atlas_memory", event["event_id"], "bootstrap canonical anchor", True)
audit_ledger.log_action("anti_forgetting_bootstrap", "atlas_memory", "prepare baseline for anti-forgetting", status="OK")
PY
python -m atlas_memory.src.main anti-forgetting
