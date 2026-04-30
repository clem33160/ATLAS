from __future__ import annotations

import json
import os
import subprocess

from atlas_memory.src.common import RUNTIME_PATHS, ensure_runtime_structure, read_jsonl, write_json


def run_capture(cmd: str) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, shell=True, text=True, capture_output=True, env=os.environ.copy())


def run(cmd: str) -> None:
    subprocess.run(cmd, shell=True, check=True, env=os.environ.copy())


def seed_demo_and_real():
    ensure_runtime_structure()
    real_event = {"event_id": "event_real", "domain": "prod", "source": "user", "content": "real", "tags": [], "metadata": {}}
    demo_event = {"event_id": "event_demo", "domain": "demo_domain", "source": "demo", "content": "client cherche plombier Lyon fuite urgente", "tags": ["demo"], "metadata": {"mode": "test"}}
    RUNTIME_PATHS["raw"].write_text("\n".join(json.dumps(x) for x in [real_event, demo_event]) + "\n", encoding="utf-8")
    RUNTIME_PATHS["semantic"].write_text(json.dumps({"source_event_id": "event_demo", "source": "demo"}) + "\n", encoding="utf-8")
    RUNTIME_PATHS["conflict"].write_text(json.dumps({"source_a": "demo", "source_b": "test", "status": "OPEN"}) + "\n", encoding="utf-8")
    RUNTIME_PATHS["uncertainty"].write_text(json.dumps({"domain": "test_domain", "status": "OPEN"}) + "\n", encoding="utf-8")
    RUNTIME_PATHS["audit"].write_text(json.dumps({"source": "cmd_demo"}) + "\n", encoding="utf-8")
    RUNTIME_PATHS["objectives"].write_text(json.dumps({"title": "demo objective", "metadata": {"source": "demo"}}) + "\n", encoding="utf-8")
    RUNTIME_PATHS["procedures"].write_text(json.dumps({"procedure_id": "test_proc", "domain": "test"}) + "\n", encoding="utf-8")
    RUNTIME_PATHS["temporal"].write_text(json.dumps({"domain": "demo"}) + "\n", encoding="utf-8")
    RUNTIME_PATHS["simulation"].write_text(json.dumps({"domain": "demo"}) + "\n", encoding="utf-8")
    write_json(RUNTIME_PATHS["active"], {"source": "demo"})


def test_demo_idempotent_and_reset_cleans_demo_keeps_real():
    run("bash atlas_memory/scripts/memory_demo.sh")
    run("bash atlas_memory/scripts/memory_demo.sh")
    run("bash atlas_memory/scripts/memory_demo.sh")
    ensure_runtime_structure()
    events = [e for e in read_jsonl(RUNTIME_PATHS["raw"]) if e.get("source") == "demo" and e.get("content") == "client cherche plombier Lyon fuite urgente"]
    assert len(events) == 1

    seed_demo_and_real()
    run("bash atlas_memory/scripts/memory_reset_demo_safe.sh")
    assert all("demo" not in str(x).lower() for x in read_jsonl(RUNTIME_PATHS["semantic"]))
    assert all("demo" not in str(x).lower() for x in read_jsonl(RUNTIME_PATHS["conflict"]))
    assert all("demo" not in str(x).lower() for x in read_jsonl(RUNTIME_PATHS["uncertainty"]))
    assert all("demo" not in str(x).lower() for x in read_jsonl(RUNTIME_PATHS["audit"]))
    assert all("demo" not in str(x).lower() for x in read_jsonl(RUNTIME_PATHS["objectives"]))
    assert all("test" not in str(x).lower() for x in read_jsonl(RUNTIME_PATHS["procedures"]))
    raw = read_jsonl(RUNTIME_PATHS["raw"])
    assert any(r.get("event_id") == "event_real" for r in raw)
    assert all(r.get("event_id") != "event_demo" for r in raw)


def test_health_real_demo_split():
    from atlas_memory.src import health

    ensure_runtime_structure()
    RUNTIME_PATHS["conflict"].write_text(json.dumps({"source_a": "demo", "source_b": "test", "status": "OPEN"}) + "\n", encoding="utf-8")
    RUNTIME_PATHS["uncertainty"].write_text(json.dumps({"domain": "demo", "status": "OPEN"}) + "\n", encoding="utf-8")
    RUNTIME_PATHS["audit"].write_text(json.dumps({"source": "demo"}) + "\n", encoding="utf-8")
    report = health.compute_health()
    assert report["demo_conflicts_count"] >= 1
    assert report["real_conflicts_count"] == 0
    assert report["demo_unresolved_uncertainties_count"] >= 1


def test_full_check_and_health_same_output_and_deterministic():
    first = run_capture("bash atlas_memory/scripts/memory_full_check.sh")
    second = run_capture("bash atlas_memory/scripts/memory_health.sh")
    third = run_capture("bash atlas_memory/scripts/memory_full_check.sh")
    assert first.returncode == 0
    assert second.returncode == 0
    assert third.returncode == 0
    a = json.loads(first.stdout)
    b = json.loads(second.stdout)
    c = json.loads(third.stdout)
    assert a["memory_score"] == b["memory_score"] == c["memory_score"]
    assert a["anti_forgetting_ok"] is True
    assert a["global_index_ok"] is True


def test_quarantine_not_counted_as_real_conflicts():
    ensure_runtime_structure()
    RUNTIME_PATHS["conflict"].write_text(json.dumps({"source_a": "source_a", "source_b": "source_b", "claim_a": "x", "claim_b": "y", "status": "OPEN"}) + "\n", encoding="utf-8")
    r = run_capture("bash atlas_memory/scripts/memory_full_check.sh")
    assert r.returncode == 0
    out = json.loads(r.stdout)
    assert out["real_conflicts_count"] == 0
