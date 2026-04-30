from __future__ import annotations

from . import active_context, canon_store, doctrine_check, objective_store
from .common import RUNTIME_PATHS, read_json, read_jsonl, write_json
from .noise_guard import should_count_as_real

REQUIRED_OBJECTIVE_TOKENS = [
    "infrastructure d'intelligence universelle",
    "mémoire canonique",
    "gouvernance anti-chaos",
    "rapporteur d’affaires",
    "génération de revenus",
    "atlas business",
    "simulation",
]
REQUIRED_INVARIANTS = {
    "append_only",
    "no_fake_proofs",
    "no_active_noise",
    "human_validation_for_canon",
    "one_domain_one_authority",
    "no_runtime_pollution",
    "no_destructive_delete",
    "provenance_required",
    "uncertainty_tracked",
    "conflicts_are_official_objects",
}
FORBIDDEN_CANON_TOKENS = ("example.com", "source_a", "source_b", "claim_a", "claim_b", "missing_evidence=proof")


def verify_core_objectives() -> bool:
    corpus = " ".join(
        f"{o.get('title', '')} {o.get('description', '')}".lower()
        for o in objective_store.list_objectives()
        if should_count_as_real(o)
    )
    return all(token in corpus for token in REQUIRED_OBJECTIVE_TOKENS)


def verify_core_invariants() -> bool:
    ctx = active_context.load_active_context()
    rules = set(ctx.get("regles_importantes", []))
    return REQUIRED_INVARIANTS.issubset(rules)


def verify_canon_presence() -> bool:
    domains = canon_store.list_canon_domains()
    if not domains:
        return False
    for domain in domains:
        canon = canon_store.get_canon(domain)
        blob = str(canon).lower()
        if any(token in blob for token in FORBIDDEN_CANON_TOKENS):
            return False
    return True


def verify_audit_presence() -> bool:
    rows = read_jsonl(RUNTIME_PATHS["audit"])
    required = ("reason", "domain", "status", "created_at")
    return len(rows) > 0 and any(all(r in row for r in required) for row in rows)


def verify_index_presence() -> bool:
    # Index generation is enforced later in the official full-check pipeline.
    return RUNTIME_PATHS["index"].parent.exists()


def verify_active_context() -> bool:
    ctx = active_context.load_active_context()
    required = ("objectif_actuel", "domain", "regles_importantes", "risques_immediats", "connaissances_pertinentes")
    return all(k in ctx and ctx.get(k) for k in required)


def verify_anti_noise() -> bool:
    active_keys = ("raw", "conflict", "uncertainty", "audit", "objectives", "procedures")
    for key in active_keys:
        for item in read_jsonl(RUNTIME_PATHS[key]):
            if not should_count_as_real(item):
                return False
    return True


def run_anti_forgetting_check() -> dict:
    doctrine = doctrine_check.run_doctrine_check()
    report = {
        "core_objectives_ok": verify_core_objectives(),
        "core_invariants_ok": verify_core_invariants(),
        "canon_ok": verify_canon_presence(),
        "audit_ok": verify_audit_presence(),
        "index_ok": verify_index_presence(),
        "doctrine_ok": doctrine.get("doctrine_ok", False),
        "active_context_ok": verify_active_context(),
        "anti_noise_ok": verify_anti_noise(),
    }
    report["anti_forgetting_ok"] = all(report.values())
    out = RUNTIME_PATHS["health_json"].parents[0] / "anti_forgetting_report.json"
    write_json(out, report)
    out.with_suffix(".md").write_text("\n".join(["# Anti Forgetting"] + [f"- {k}: {v}" for k, v in report.items()]), encoding="utf-8")
    return report
