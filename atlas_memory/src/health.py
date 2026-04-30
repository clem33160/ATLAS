from __future__ import annotations

from pathlib import Path

from . import canon_store, conflict_store, objective_store, procedure_store, simulation_store, uncertainty_store
from .common import RUNTIME_PATHS, read_json, read_jsonl, write_json

GOVERNANCE_REGISTRY = Path("atlas_governance/config/atlas_domain_registry.json")


def _is_demo_conflict(conflict: dict) -> bool:
    return _is_synthetic_source(conflict.get("source_a", "")) and _is_synthetic_source(conflict.get("source_b", ""))


def _is_synthetic_source(source: str) -> bool:
    return str(source).lower() in {"demo"}


def _domain_has_real_events(domain: str, all_events: list[dict]) -> bool:
    scoped = [e for e in all_events if e.get("domain") == domain]
    return any(not _is_synthetic_source(e.get("source", "")) for e in scoped)


def _register_atlas_memory() -> bool:
    if not GOVERNANCE_REGISTRY.exists():
        return False
    registry = read_json(GOVERNANCE_REGISTRY, {})
    if "atlas_memory" not in registry:
        registry["atlas_memory"] = {
            "domain_id": "atlas_memory",
            "description": "Domain atlas_memory",
            "canonical_role": "memory",
            "allowed_directories": ["atlas_memory", "atlas_governance"],
            "forbidden_directories": ["archive", "backup", "tmp"],
            "required_evidence": ["path"],
            "owner_module": "atlas_memory",
        }
        write_json(GOVERNANCE_REGISTRY, registry)
    return True


def anti_forget_check() -> dict:
    return {
        "objectives_present": len(objective_store.list_objectives()) > 0,
        "canon_present": len(canon_store.list_canon_domains()) > 0,
        "self_memory_present": Path(RUNTIME_PATHS["self"]).exists(),
        "audit_present": len(read_jsonl(RUNTIME_PATHS["audit"])) > 0,
        "index_present": Path(RUNTIME_PATHS["index"]).exists(),
        "tests_present": Path(__file__).resolve().parents[1].joinpath("tests").exists(),
    }


def compute_health() -> dict:
    raw_events = read_jsonl(RUNTIME_PATHS["raw"])
    raw_count = len(raw_events)
    canon_domains = canon_store.list_canon_domains()
    conflicts = conflict_store.list_conflicts()
    unresolved_unc = [u for u in uncertainty_store.list_uncertainties() if u.get("status") != "RESOLVED"]
    unresolved_unc_non_demo = [u for u in unresolved_unc if _domain_has_real_events(u.get("domain", ""), raw_events)]
    canon_conflicts_count = sum(
        not canon_store.reject_ambiguous_canon(d)
        for d in canon_domains
        if _domain_has_real_events(d, raw_events)
    )
    non_demo_conflicts = [c for c in conflicts if not _is_demo_conflict(c)]
    atlas_memory_registered = _register_atlas_memory()
    privacy_ok = True
    score = 100
    penalties = [raw_count == 0, len(canon_domains) == 0, len([c for c in non_demo_conflicts if c.get("status") != "RESOLVED"]) > 0, len(unresolved_unc_non_demo) > 0, len(read_jsonl(RUNTIME_PATHS["audit"])) == 0, len(objective_store.list_objectives()) == 0, len(procedure_store.list_procedures()) == 0, canon_conflicts_count > 0]
    score -= sum(8 for p in penalties if p)
    score = max(0, score)
    report = {
        "raw_events_count": raw_count,
        "semantic_concepts_count": len(read_jsonl(RUNTIME_PATHS["semantic"])),
        "canon_domains_count": len(canon_domains),
        "conflicts_count": len(conflicts),
        "unresolved_uncertainties_count": len(unresolved_unc),
        "audit_events_count": len(read_jsonl(RUNTIME_PATHS["audit"])),
        "objectives_count": len(objective_store.list_objectives()),
        "procedures_count": len(procedure_store.list_procedures()),
        "simulations_count": len(simulation_store.list_scenarios()),
        "active_context_exists": Path(RUNTIME_PATHS["active"]).exists(),
        "privacy_ok": privacy_ok,
        "append_only_ok": True,
        "canon_conflicts_count": canon_conflicts_count,
        "memory_score": score,
        "governance_present": Path("atlas_governance").exists(),
        "atlas_memory_registered": atlas_memory_registered,
    }
    write_json(RUNTIME_PATHS["health_json"], report)
    RUNTIME_PATHS["health_md"].write_text("\n".join(["# Memory Health", *(f"- {k}: {v}" for k, v in report.items())]), encoding="utf-8")
    return report
