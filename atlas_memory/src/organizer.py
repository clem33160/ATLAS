from __future__ import annotations

from . import canon_store, raw_store


def classify_importance(item: dict) -> str:
    text = str(item).lower()
    if "invariant" in text:
        return "IDENTITY_INVARIANT"
    if item.get("status") == "CANON":
        return "RULE"
    return "FACT"


def build_hierarchy_summary(domain: str | None = None) -> dict:
    events = raw_store.list_events(domain=domain, limit=500)
    return {"RAW": len(events), "FACT": sum(classify_importance(e) == "FACT" for e in events), "RULE": len(canon_store.list_canon_domains())}


def find_unclassified_items() -> list[dict]:
    return [e for e in raw_store.list_events(limit=500) if not e.get("tags")]


def suggest_organization() -> list[dict]:
    return [{"event_id": e["event_id"], "suggestion": "add_tags"} for e in find_unclassified_items()[:20]]


def classify_noise_item(item: dict) -> str:
    if item.get("confidence", 1) < 0.3:
        return "weak_hypothesis"
    return "unverified" if not item.get("validated_by_human") else "noise"


def classify_noise() -> list[dict]:
    return [{"event_id": e["event_id"], "class": classify_noise_item(e)} for e in raw_store.list_events(limit=500)]


def list_noise_candidates() -> list[dict]:
    return [n for n in classify_noise() if n["class"] in {"weak_hypothesis", "unverified", "duplicate", "conflict", "archive"}]


def suggest_canon_candidates() -> list[dict]:
    return [e for e in raw_store.list_events(limit=200) if e.get("confidence", 0) > 0.8 and e.get("validated_by_human")]


def rank_memory_value(item: dict) -> str:
    if "Atlas n’est pas un simple chatbot" in str(item):
        return "CRITICAL"
    if item.get("kind") == "error":
        return "IMPORTANT"
    return "USEFUL"
