from __future__ import annotations

from .common import RUNTIME_PATHS, append_jsonl, new_id, now_iso, read_jsonl


def open_conflict(source_a: str, source_b: str, claim_a: str, claim_b: str, domain: str) -> dict:
    payload = {
        "conflict_id": new_id("conflict"),
        "source_a": source_a,
        "source_b": source_b,
        "date_a": now_iso(),
        "date_b": now_iso(),
        "reliability_a": 0.5,
        "reliability_b": 0.5,
        "claim_a": claim_a,
        "claim_b": claim_b,
        "domain": domain,
        "impact": "MEDIUM",
        "decision": "PENDING",
        "status": "OPEN",
    }
    append_jsonl(RUNTIME_PATHS["conflict"], payload)
    return payload


def list_conflicts(status: str | None = None) -> list[dict]:
    rows = read_jsonl(RUNTIME_PATHS["conflict"])
    if status:
        return [r for r in rows if r.get("status") == status]
    return rows


def detect_conflicts() -> list[dict]:
    return [c for c in list_conflicts() if c.get("claim_a") != c.get("claim_b")]


def resolve_conflict(conflict_id: str, decision: str, reason: str, human_validated: bool = False) -> dict | None:
    rows = list_conflicts()
    found = None
    for row in rows:
        if row["conflict_id"] == conflict_id:
            row["status"] = "RESOLVED"
            row["decision"] = decision
            row["reason"] = reason
            row["human_validated"] = human_validated
            found = row
    if found:
        RUNTIME_PATHS["conflict"].write_text("", encoding="utf-8")
        for row in rows:
            append_jsonl(RUNTIME_PATHS["conflict"], row)
    return found
