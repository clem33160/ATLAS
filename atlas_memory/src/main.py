from __future__ import annotations

import argparse
import json
from pathlib import Path

from . import active_context, anti_forgetting, audit_ledger, canon_store, health, objective_store, procedure_store, raw_store, self_memory, semantic_store
from .common import RUNTIME_PATHS, ensure_runtime_structure, new_id, now_iso, read_json, read_jsonl


def cmd_init(_: argparse.Namespace) -> None:
    ensure_runtime_structure()
    self_memory.init_self_memory()
    procedure_store.add_procedure("qualify_lead", "rapporteur_affaires", ["collect", "score"], ["bad_source"], ["manual_review"])
    procedure_store.add_procedure("promote_to_canon", "memory", ["validate", "promote"], ["canon_conflict"], ["health"])
    procedure_store.add_procedure("audit_system", "memory", ["scan", "report"], ["blind_spot"], ["health"])
    procedure_store.add_procedure("resolve_conflict", "memory", ["compare", "decide"], ["wrong_resolution"], ["human_validation"])
    procedure_store.add_procedure("build_active_context", "memory", ["collect", "save"], ["missing_rule"], ["load"])
    top = objective_store.add_objective("SUPREME", "Atlas infrastructure", "Construire Atlas comme infrastructure d'intelligence universelle")
    for t in ["mémoire canonique", "gouvernance anti-chaos", "rapporteur d’affaires", "génération de revenus", "Atlas Business", "simulation", "data center / robotique / science"]:
        objective_store.add_objective("PROGRAM", t, t, parent_id=top["objective_id"])


def cmd_ingest(args: argparse.Namespace) -> None:
    event = {"event_id": new_id("event"), "created_at": now_iso(), "kind": args.kind, "domain": args.domain, "content": args.content, "source": args.source, "source_url": None, "confidence": args.confidence, "evidence_ids": [], "linked_objective_ids": [], "validated_by_human": False, "risk_level": "LOW", "useful_for_future": True, "status": "RAW", "tags": [], "metadata": {}}
    raw_store.append_event(event)
    facts = semantic_store.extract_semantic_facts(event)
    semantic_store.append_concepts(event["event_id"], facts)
    audit_ledger.log_action("ingest", args.domain, "cli ingest", files=[])
    print(json.dumps(event))


def cmd_query(args):
    print(json.dumps(raw_store.list_events(domain=args.domain, limit=args.limit), indent=2, ensure_ascii=False))


def cmd_promote(args):
    print(json.dumps(canon_store.promote_to_canon(args.domain, args.event_id, args.reason, args.human_validated), indent=2, ensure_ascii=False))


def cmd_active(args):
    ctx = active_context.build_active_context(args.task, args.domain)
    active_context.save_active_context(ctx)
    print(json.dumps(ctx, indent=2, ensure_ascii=False))


def cmd_health(_: argparse.Namespace):
    print(json.dumps(health.compute_health(), indent=2, ensure_ascii=False))

def cmd_anti_forgetting(_: argparse.Namespace):
    print(json.dumps(anti_forgetting.run_anti_forgetting_check(), indent=2, ensure_ascii=False))


def cmd_demo(_: argparse.Namespace):
    cmd_init(argparse.Namespace())
    demo_content = "client cherche plombier Lyon fuite urgente"
    existing_demo = [
        e for e in read_jsonl(RUNTIME_PATHS["raw"])
        if e.get("source") == "demo"
        and e.get("domain") == "rapporteur_affaires"
        and e.get("kind") == "conversation"
        and e.get("content") == demo_content
    ]
    if existing_demo:
        evt = existing_demo[-1]
    else:
        cmd_ingest(argparse.Namespace(kind="conversation", domain="rapporteur_affaires", content=demo_content, source="demo", confidence=0.9))
        evt = raw_store.list_events(limit=1)[0]
    canon = canon_store.get_canon("rapporteur_affaires")
    if not any(e.get("event_id") == evt["event_id"] for e in canon.get("entries", [])):
        canon_store.promote_to_canon("rapporteur_affaires", evt["event_id"], "validated memory", True)
    cmd_active(argparse.Namespace(task="améliorer rapporteur affaires", domain="rapporteur_affaires"))
    cmd_health(argparse.Namespace())


def cmd_ingest_rapporteur(_: argparse.Namespace):
    base = Path("atlas_rapporteur/runtime")
    files = [base / "reports/daily_report.md", base / "exports/leads_ranked.json", base / "audit/rejected_results.json"]
    for path in files:
        if path.exists():
            content = path.read_text(encoding="utf-8")[:1000]
            raw_store.append_event({"event_id": new_id("event"), "created_at": now_iso(), "kind": "file", "domain": "rapporteur_affaires", "content": content, "source": str(path), "source_url": None, "confidence": 0.7, "evidence_ids": [], "linked_objective_ids": [], "validated_by_human": False, "risk_level": "LOW", "useful_for_future": True, "status": "RAW", "tags": ["rapporteur"], "metadata": {}})


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("init").set_defaults(func=cmd_init)
    p=sub.add_parser("ingest"); p.add_argument("--kind", required=True); p.add_argument("--domain", required=True); p.add_argument("--content", required=True); p.add_argument("--source", default="cli"); p.add_argument("--confidence", type=float, default=0.7); p.set_defaults(func=cmd_ingest)
    q=sub.add_parser("query"); q.add_argument("--domain"); q.add_argument("--limit", type=int, default=50); q.set_defaults(func=cmd_query)
    c=sub.add_parser("promote-canon"); c.add_argument("--domain", required=True); c.add_argument("--event-id", required=True); c.add_argument("--reason", required=True); c.add_argument("--human-validated", action="store_true"); c.set_defaults(func=cmd_promote)
    a=sub.add_parser("active-context"); a.add_argument("--task", required=True); a.add_argument("--domain"); a.set_defaults(func=cmd_active)
    sub.add_parser("health").set_defaults(func=cmd_health)
    sub.add_parser("anti-forgetting").set_defaults(func=cmd_anti_forgetting)
    sub.add_parser("demo").set_defaults(func=cmd_demo)
    sub.add_parser("ingest-rapporteur").set_defaults(func=cmd_ingest_rapporteur)
    args = parser.parse_args(); ensure_runtime_structure(); args.func(args)

if __name__ == "__main__":
    main()
