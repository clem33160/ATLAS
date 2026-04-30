from __future__ import annotations

from .common import RUNTIME_PATHS, append_jsonl, now_iso, read_jsonl


def append_timeline_event(title: str, domain: str, event_type: str, before=None, after=None) -> dict:
    payload = {"title": title, "domain": domain, "event_type": event_type, "before": before, "after": after, "created_at": now_iso(), "reason": "state_transition"}
    append_jsonl(RUNTIME_PATHS["temporal"], payload)
    return payload


def list_timeline(domain: str | None = None) -> list[dict]:
    rows = read_jsonl(RUNTIME_PATHS["temporal"])
    return [r for r in rows if not domain or r.get("domain") == domain]


def get_recent_changes(limit: int = 20) -> list[dict]:
    return list_timeline()[-limit:]
