from __future__ import annotations

from .common import RUNTIME_PATHS, append_jsonl, new_id, read_jsonl


def add_uncertainty(domain: str, claim: str, missing_evidence: str, confidence: float) -> dict:
    payload = {"id": new_id("unc"), "domain": domain, "claim": claim, "missing_evidence": missing_evidence, "confidence": confidence, "status": "OPEN"}
    append_jsonl(RUNTIME_PATHS["uncertainty"], payload)
    return payload


def resolve_uncertainty(id: str, resolution: str, evidence_id: str | None = None) -> dict | None:
    rows = read_jsonl(RUNTIME_PATHS["uncertainty"])
    found = None
    for row in rows:
        if row["id"] == id:
            row["status"] = "RESOLVED"
            row["resolution"] = resolution
            row["evidence_id"] = evidence_id
            found = row
    if found:
        RUNTIME_PATHS["uncertainty"].write_text("", encoding="utf-8")
        for row in rows:
            append_jsonl(RUNTIME_PATHS["uncertainty"], row)
    return found


def list_uncertainties(domain: str | None = None) -> list[dict]:
    rows = read_jsonl(RUNTIME_PATHS["uncertainty"])
    return [r for r in rows if not domain or r.get("domain") == domain]
