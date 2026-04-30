from __future__ import annotations

from .common import RUNTIME_PATHS, append_jsonl, read_jsonl


def add_evidence(event_id: str, proof: str, source: str, confidence: float) -> dict:
    payload = {"event_id": event_id, "proof": proof, "source": source, "confidence": confidence}
    append_jsonl(RUNTIME_PATHS["evidence"], payload)
    return payload


def list_evidence(event_id: str | None = None) -> list[dict]:
    rows = read_jsonl(RUNTIME_PATHS["evidence"])
    if event_id:
        return [r for r in rows if r.get("event_id") == event_id]
    return rows
