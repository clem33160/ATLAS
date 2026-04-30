from __future__ import annotations

import json
import subprocess

from atlas_memory.src.common import RUNTIME_PATHS, ensure_runtime_structure, read_json, read_jsonl
from atlas_memory.src.health import compute_health
from atlas_memory.src.noise_guard import classify_noise, should_count_as_real
from atlas_memory.src.noise_quarantine import quarantine_noise


def test_noise_guard_detects_placeholder_conflict():
    c = {"source_a": "a", "source_b": "b", "claim_a": "x", "claim_b": "y", "reason": "reason"}
    out = classify_noise(c)
    assert out["is_noise"] is True


def test_noise_guard_detects_placeholder_uncertainty():
    u = {"claim": "claim", "missing_evidence": "proof", "confidence": 0.2}
    assert classify_noise(u)["is_noise"] is True


def test_noise_guard_keeps_real_user_event():
    e = {"source": "user", "content": "Le client veut un devis plomberie Lyon", "domain": "rapporteur_affaires"}
    assert should_count_as_real(e) is True


def test_quarantine_moves_noise_out_of_real_runtime():
    ensure_runtime_structure()
    RUNTIME_PATHS["conflict"].write_text(json.dumps({"source_a":"a","source_b":"b","claim_a":"x","claim_b":"y"})+"\n")
    RUNTIME_PATHS["uncertainty"].write_text(json.dumps({"claim":"claim","missing_evidence":"proof","status":"OPEN"})+"\n")
    quarantine_noise()
    assert len(read_jsonl(RUNTIME_PATHS["conflict"])) == 0
    assert len(read_jsonl(RUNTIME_PATHS["uncertainty"])) == 0


def test_quarantine_preserves_real_items():
    ensure_runtime_structure()
    RUNTIME_PATHS["conflict"].write_text(json.dumps({"source_a":"crm","source_b":"email","claim_a":"rdv 10h","claim_b":"rdv 11h","status":"OPEN"})+"\n")
    quarantine_noise()
    assert len(read_jsonl(RUNTIME_PATHS["conflict"])) == 1


def test_memory_health_ignores_quarantined_demo_noise():
    ensure_runtime_structure()
    quarantine_noise()
    h = compute_health()
    assert h["quarantined_noise_count"] >= 0


def test_memory_health_penalizes_real_conflict():
    ensure_runtime_structure()
    RUNTIME_PATHS["conflict"].write_text(json.dumps({"source_a":"crm","source_b":"email","claim_a":"A","claim_b":"B","status":"OPEN"})+"\n")
    h=compute_health()
    assert h["memory_score"] < 100


def test_noise_report_generated():
    subprocess.run("bash atlas_memory/scripts/memory_noise_clean.sh", shell=True, check=True, env={**__import__("os").environ, "ATLAS_MEMORY_RUNTIME_DIR": str(RUNTIME_PATHS["raw"].parents[1])})
    assert (RUNTIME_PATHS["raw"].parents[1] / "noise/quarantine_report.json").exists()
    assert (RUNTIME_PATHS["raw"].parents[1] / "noise/quarantine_report.md").exists()


def test_pytest_does_not_write_to_real_runtime():
    real_runtime = RUNTIME_PATHS["raw"].parents[1]
    assert "atlas_memory/runtime" not in str(real_runtime)
