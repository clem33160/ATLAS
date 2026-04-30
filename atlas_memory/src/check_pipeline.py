from __future__ import annotations

import argparse

from . import active_context, anti_forgetting, audit_ledger, canon_store, doctrine_check, health, raw_store
from .common import RUNTIME_PATHS, ensure_runtime_structure, new_id, now_iso, read_jsonl, write_json
from .global_index import generate_global_index
from .integrity_check import run_integrity_check
from .main import cmd_init
from .noise_quarantine import quarantine_noise


def _ensure_bootstrap_anchor() -> None:
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
            "source": "atlas_memory/src/check_pipeline.py",
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

    audit_rows = read_jsonl(RUNTIME_PATHS["audit"])
    if not any(a.get("reason") == "anti_forgetting_bootstrap" and a.get("domain") == "atlas_memory" for a in audit_rows):
        audit_ledger.log_action("anti_forgetting_bootstrap", "atlas_memory", "prepare baseline for anti-forgetting", status="OK")


def run_memory_full_check(clean_noise: bool = True, bootstrap: bool = True, regenerate_index: bool = True) -> dict:
    ensure_runtime_structure()
    quarantine_report = quarantine_noise() if clean_noise else {}

    if bootstrap:
        if not read_jsonl(RUNTIME_PATHS["objectives"]) or not read_jsonl(RUNTIME_PATHS["procedures"]):
            cmd_init(argparse.Namespace())
        _ensure_bootstrap_anchor()

    ctx = active_context.build_active_context("maintain atlas memory core", "atlas_memory")
    active_context.save_active_context(ctx)

    doctrine = doctrine_check.run_doctrine_check()
    anti = anti_forgetting.run_anti_forgetting_check()
    index = generate_global_index() if regenerate_index else {}
    integrity = run_integrity_check()
    health_report = health.compute_health()

    final = {
        **health_report,
        "doctrine_ok": doctrine.get("doctrine_ok", False),
        "anti_forgetting_ok": anti.get("anti_forgetting_ok", False),
        "global_index_ok": bool(integrity.get("global_index_ok", False)),
        "quarantined_noise_count": quarantine_report.get("quarantined_noise_count", health_report.get("quarantined_noise_count", 0)),
        "pipeline_index_generated": bool(index),
    }
    write_json(RUNTIME_PATHS["health_json"], final)
    return final
