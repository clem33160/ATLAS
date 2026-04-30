from __future__ import annotations

from pathlib import Path

from .common import RUNTIME_PATHS, read_json, write_json


def _canon_file(domain: str) -> Path:
    return RUNTIME_PATHS["canon"] / f"{domain}.json"


def promote_to_canon(domain: str, event_id: str, reason: str, human_validated: bool = False) -> dict:
    canon = read_json(_canon_file(domain), {"domain": domain, "entries": []})
    canon["entries"].append({
        "event_id": event_id,
        "reason": reason,
        "human_validated": human_validated,
        "active": True,
    })
    write_json(_canon_file(domain), canon)
    return canon


def get_canon(domain: str) -> dict:
    return read_json(_canon_file(domain), {"domain": domain, "entries": []})


def list_canon_domains() -> list[str]:
    return sorted([p.stem for p in RUNTIME_PATHS["canon"].glob("*.json")])


def reject_ambiguous_canon(domain: str) -> bool:
    canon = get_canon(domain)
    return sum(1 for e in canon.get("entries", []) if e.get("active")) <= 1
