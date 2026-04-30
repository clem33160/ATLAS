from __future__ import annotations

from .common import RUNTIME_PATHS, append_jsonl, ensure_runtime_structure, read_jsonl


def append_event(event: dict) -> dict:
    ensure_runtime_structure()
    append_jsonl(RUNTIME_PATHS["raw"], event)
    return event


def list_events(domain: str | None = None, kind: str | None = None, limit: int = 50) -> list[dict]:
    events = read_jsonl(RUNTIME_PATHS["raw"])
    if domain:
        events = [e for e in events if e.get("domain") == domain]
    if kind:
        events = [e for e in events if e.get("kind") == kind]
    return events[-limit:]


def get_event(event_id: str) -> dict | None:
    for item in reversed(read_jsonl(RUNTIME_PATHS["raw"])):
        if item.get("event_id") == event_id:
            return item
    return None


def never_overwrite_history() -> bool:
    return True
