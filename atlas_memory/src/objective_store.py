from __future__ import annotations

from .common import RUNTIME_PATHS, append_jsonl, new_id, read_jsonl


def add_objective(level: str, title: str, description: str, parent_id: str | None = None) -> dict:
    payload = {"objective_id": new_id("obj"), "level": level, "title": title, "description": description, "parent_id": parent_id, "status": "OPEN", "notes": []}
    append_jsonl(RUNTIME_PATHS["objectives"], payload)
    return payload


def list_objectives(level: str | None = None) -> list[dict]:
    rows = read_jsonl(RUNTIME_PATHS["objectives"])
    return [r for r in rows if not level or r.get("level") == level]


def mark_progress(objective_id: str, status: str, note: str) -> dict | None:
    rows = read_jsonl(RUNTIME_PATHS["objectives"])
    found = None
    for row in rows:
        if row["objective_id"] == objective_id:
            row["status"] = status
            row.setdefault("notes", []).append(note)
            found = row
    if found:
        RUNTIME_PATHS["objectives"].write_text("", encoding="utf-8")
        for row in rows:
            append_jsonl(RUNTIME_PATHS["objectives"], row)
    return found
