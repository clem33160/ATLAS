from __future__ import annotations

from .common import RUNTIME_PATHS, append_jsonl, read_jsonl


def infer_causal_links(events: list[dict]) -> list[dict]:
    links: list[dict] = []
    for idx in range(1, len(events)):
        prev = events[idx - 1]
        curr = events[idx]
        if prev.get("domain") != curr.get("domain"):
            continue
        if prev.get("source") == "demo" or curr.get("source") == "demo":
            continue
        hypothesis = f"{prev.get('kind','event')} -> {curr.get('kind','event')}"
        confidence = 0.72 if curr.get("kind") in {"lead_accepted", "governance_decision"} else 0.61
        links.append({
            "cause_event_id": prev.get("event_id"),
            "effect_event_id": curr.get("event_id"),
            "hypothesis": hypothesis,
            "confidence": confidence,
            "domain": curr.get("domain", "general"),
        })
    return links


def persist_causal_links(links: list[dict]) -> int:
    count = 0
    for link in links:
        if not link.get("cause_event_id") or not link.get("effect_event_id"):
            continue
        append_jsonl(RUNTIME_PATHS["causal"], link)
        count += 1
    return count


def list_causal_links(domain: str | None = None) -> list[dict]:
    rows = read_jsonl(RUNTIME_PATHS["causal"])
    if not domain:
        return rows
    return [r for r in rows if r.get("domain") == domain]
