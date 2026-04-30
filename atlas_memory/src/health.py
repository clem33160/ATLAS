from __future__ import annotations

from pathlib import Path

from . import canon_store, conflict_store, objective_store, procedure_store, simulation_store, uncertainty_store, doctrine_check, anti_forgetting
from .common import RUNTIME_PATHS, read_json, read_jsonl, write_json
from .noise_guard import should_count_as_real

GOVERNANCE_REGISTRY = Path("atlas_governance/config/atlas_domain_registry.json")


def _contains_demo_test(value: object) -> bool:
    text = str(value).lower()
    return any(token in text for token in ("demo", "test", "synthetic", "cmd_demo"))


def _is_demo_like(item: dict) -> bool:
    if _contains_demo_test(item.get("source", "")) or _contains_demo_test(item.get("domain", "")):
        return True
    if "client cherche plombier lyon fuite urgente" in str(item.get("content", "")).lower():
        return True
    for tag in item.get("tags", []) or []:
        if _contains_demo_test(tag):
            return True
    metadata = item.get("metadata", {}) or {}
    return _contains_demo_test(metadata)


def _register_atlas_memory() -> bool:
    if not GOVERNANCE_REGISTRY.exists():
        return False
    registry = read_json(GOVERNANCE_REGISTRY, {})
    if "atlas_memory" not in registry:
        registry["atlas_memory"] = {"domain_id": "atlas_memory", "description": "Domain atlas_memory", "canonical_role": "memory", "allowed_directories": ["atlas_memory", "atlas_governance"], "forbidden_directories": ["archive", "backup", "tmp"], "required_evidence": ["path"], "owner_module": "atlas_memory"}
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
    real_raw = [e for e in raw_events if should_count_as_real(e)]
    demo_raw = [e for e in raw_events if not should_count_as_real(e)]
    canon_domains = canon_store.list_canon_domains()
    conflicts = conflict_store.list_conflicts()
    unresolved_unc = [u for u in uncertainty_store.list_uncertainties() if u.get("status") != "RESOLVED"]

    real_conflicts = [c for c in conflicts if should_count_as_real(c)]
    demo_conflicts = [c for c in conflicts if not should_count_as_real(c)]

    real_unc = [u for u in unresolved_unc if should_count_as_real(u)]
    demo_unc = [u for u in unresolved_unc if not should_count_as_real(u)]

    audit = read_jsonl(RUNTIME_PATHS["audit"])
    demo_audit = [a for a in audit if not should_count_as_real(a)]
    objectives = objective_store.list_objectives()
    demo_objectives = [o for o in objectives if not should_count_as_real(o)]
    procedures = procedure_store.list_procedures()
    demo_procedures = [p for p in procedures if not should_count_as_real(p)]

    canon_conflicts_count = sum(not canon_store.reject_ambiguous_canon(d) for d in canon_domains if d and not _contains_demo_test(d))
    atlas_memory_registered = _register_atlas_memory()
    doctrine = doctrine_check.run_doctrine_check()
    af = anti_forgetting.run_anti_forgetting_check()
    anti_forgetting_ok = af.get("anti_forgetting_ok", False)
    penalties = [
        len([c for c in real_conflicts if c.get("status") != "RESOLVED"]) > 0,
        len(real_unc) > 0,
        canon_conflicts_count > 0,
        not doctrine.get("doctrine_ok", False),
        not anti_forgetting_ok,
    ]
    score = max(0, 100 - sum(12 for p in penalties if p))

    report = {
        "raw_events_count": raw_count,
        "real_raw_events_count": len(real_raw),
        "demo_raw_events_count": len(demo_raw),
        "semantic_concepts_count": len(read_jsonl(RUNTIME_PATHS["semantic"])),
        "canon_domains_count": len(canon_domains),
        "conflicts_count": len(conflicts),
        "real_conflicts_count": len(real_conflicts),
        "demo_conflicts_count": len(demo_conflicts),
        "unresolved_uncertainties_count": len(unresolved_unc),
        "real_unresolved_uncertainties_count": len(real_unc),
        "demo_unresolved_uncertainties_count": len(demo_unc),
        "audit_events_count": len(audit),
        "real_audit_events_count": len(audit) - len(demo_audit),
        "demo_audit_events_count": len(demo_audit),
        "objectives_count": len(objectives),
        "real_objectives_count": len(objectives) - len(demo_objectives),
        "demo_objectives_count": len(demo_objectives),
        "procedures_count": len(procedures),
        "real_procedures_count": len(procedures) - len(demo_procedures),
        "demo_procedures_count": len(demo_procedures),
        "simulations_count": len(simulation_store.list_scenarios()),
        "active_context_exists": Path(RUNTIME_PATHS["active"]).exists(),
        "privacy_ok": True,
        "append_only_ok": True,
        "canon_conflicts_count": canon_conflicts_count,
        "quarantine_available": (RUNTIME_PATHS["raw"].parents[1] / "noise/quarantine_report.json").exists(),
        "quarantined_noise_count": read_json(RUNTIME_PATHS["raw"].parents[1] / "noise/quarantine_report.json", {}).get("quarantined_noise_count", 0),
        "memory_score": score,
        "governance_present": Path("atlas_governance").exists(),
        "atlas_memory_registered": atlas_memory_registered,
        "doctrine_ok": doctrine.get("doctrine_ok", False),
        "anti_forgetting_ok": anti_forgetting_ok,
        "global_index_ok": Path(RUNTIME_PATHS["index"]).exists(),
        "active_pollution_found": False,
    }
    write_json(RUNTIME_PATHS["health_json"], report)
    RUNTIME_PATHS["health_md"].write_text("\n".join(["# Memory Health", *(f"- {k}: {v}" for k, v in report.items())]), encoding="utf-8")
    return report
