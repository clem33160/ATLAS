from atlas_memory.src import active_context, audit_ledger, canon_store, conflict_store, health, objective_store, procedure_store, raw_store, self_memory, semantic_store, temporal_store, uncertainty_store
from atlas_memory.src.common import RUNTIME_PATHS, ensure_runtime_structure, new_id, now_iso


def test_imports():
    import atlas_memory
    assert atlas_memory


def test_core_flow():
    ensure_runtime_structure()
    ev1 = {"event_id": new_id("event"), "created_at": now_iso(), "kind": "conversation", "domain": "rapporteur_affaires", "content": "client cherche plombier Lyon fuite urgente", "source": "t", "source_url": None, "confidence": 0.9, "evidence_ids": [], "linked_objective_ids": [], "validated_by_human": True, "risk_level": "LOW", "useful_for_future": True, "status": "RAW", "tags": [], "metadata": {}}
    ev2 = {**ev1, "event_id": new_id("event"), "content": "second"}
    raw_store.append_event(ev1); raw_store.append_event(ev2)
    assert len(raw_store.list_events(limit=2)) == 2
    facts = semantic_store.extract_semantic_facts(ev1)
    assert facts.get("trade") == "plomberie" and facts.get("city") == "Lyon"
    canon_store.promote_to_canon("rapporteur_affaires", ev1["event_id"], "ok", True)
    canon_store.promote_to_canon("rapporteur_affaires", ev2["event_id"], "ok", True)
    assert not canon_store.reject_ambiguous_canon("rapporteur_affaires")
    unc = uncertainty_store.add_uncertainty("rapporteur_affaires", "claim", "proof", 0.2)
    assert unc["status"] == "OPEN"
    conflict = conflict_store.open_conflict("a", "b", "x", "y", "d")
    assert conflict_store.resolve_conflict(conflict["conflict_id"], "keep a", "reason")
    temporal_store.append_timeline_event("t", "d", "transition", before="a", after="b")
    assert temporal_store.list_timeline("d")
    procedure_store.add_procedure("p", "d", ["s"], ["r"], ["t"])
    assert procedure_store.get_procedure("p")
    objective_store.add_objective("L1", "t", "d")
    s = self_memory.init_self_memory()
    assert "mission" in s and s["invariants"]
    ctx = active_context.build_active_context("task", "d"); active_context.save_active_context(ctx)
    assert active_context.load_active_context().get("objectif_actuel") == "task"
    audit_ledger.log_action("a", "d", "r")
    rep = health.compute_health()
    assert RUNTIME_PATHS["health_json"].exists() and RUNTIME_PATHS["health_md"].exists()
    assert rep["memory_score"] < 100


def test_privacy_and_rapporteur_ingest_no_crash():
    try:
        self_memory.add_user_preference("password", "123", consent=False)
    except ValueError:
        pass
    else:
        raise AssertionError("privacy should fail")
