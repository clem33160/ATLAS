from __future__ import annotations

from .common import RUNTIME_PATHS, append_jsonl, read_jsonl


def add_procedure(name: str, domain: str, steps: list[str], risks: list[str], tests: list[str]) -> dict:
    payload = {"name": name, "domain": domain, "steps": steps, "risks": risks, "tests": tests}
    append_jsonl(RUNTIME_PATHS["procedures"], payload)
    return payload


def list_procedures(domain: str | None = None) -> list[dict]:
    rows = read_jsonl(RUNTIME_PATHS["procedures"])
    return [r for r in rows if not domain or r.get("domain") == domain]


def get_procedure(name: str) -> dict | None:
    for row in reversed(read_jsonl(RUNTIME_PATHS["procedures"])):
        if row.get("name") == name:
            return row
    return None
