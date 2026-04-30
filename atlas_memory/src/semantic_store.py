from __future__ import annotations

from .common import RUNTIME_PATHS, append_jsonl, read_jsonl


def extract_semantic_facts(event: dict) -> dict:
    text = event.get("content", "").lower()
    concepts = []
    facts = {"event_id": event.get("event_id"), "domain": event.get("domain")}
    if "plomb" in text:
        facts["trade"] = "plomberie"
        concepts.append("plombier")
    if "lyon" in text:
        facts["city"] = "Lyon"
        concepts.append("Lyon")
    if "fuite" in text:
        concepts.append("fuite")
    if "urgent" in text or "urgence" in text:
        facts["urgency"] = "high"
        concepts.append("urgence")
    if "cherche" in text or "client" in text:
        facts["intent"] = "client_request"
    facts["concepts"] = sorted(set(concepts))
    return facts


def append_concepts(event_id: str, concepts: dict) -> dict:
    payload = {"event_id": event_id, **concepts}
    append_jsonl(RUNTIME_PATHS["semantic"], payload)
    return payload


def find_concepts(query: str) -> list[dict]:
    q = query.lower()
    return [row for row in read_jsonl(RUNTIME_PATHS["semantic"]) if q in str(row).lower()]


def append_causal_link(cause_event_id: str, effect_event_id: str, hypothesis: str, confidence: float) -> dict:
    payload = {
        "cause_event_id": cause_event_id,
        "effect_event_id": effect_event_id,
        "hypothesis": hypothesis,
        "confidence": confidence,
    }
    append_jsonl(RUNTIME_PATHS["causal"], payload)
    return payload


def list_causal_links(domain: str | None = None) -> list[dict]:
    rows = read_jsonl(RUNTIME_PATHS["causal"])
    if not domain:
        return rows
    events = {e["event_id"]: e for e in read_jsonl(RUNTIME_PATHS["raw"])}
    return [r for r in rows if events.get(r["cause_event_id"], {}).get("domain") == domain]
