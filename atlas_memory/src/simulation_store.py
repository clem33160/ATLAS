from __future__ import annotations

from .common import RUNTIME_PATHS, append_jsonl, new_id, read_jsonl


def add_scenario(title: str, assumptions: list[str], expected_outcomes: list[str], risks: list[str], cost: float, benefit: float, confidence: float, domain: str = "strategy") -> dict:
    payload = {"scenario_id": new_id("sim"), "title": title, "domain": domain, "assumptions": assumptions, "expected_outcomes": expected_outcomes, "risks": risks, "cost": cost, "benefit": benefit, "confidence": confidence}
    append_jsonl(RUNTIME_PATHS["simulation"], payload)
    return payload


def compare_scenarios(ids: list[str]) -> list[dict]:
    rows = read_jsonl(RUNTIME_PATHS["simulation"])
    chosen = [r for r in rows if r.get("scenario_id") in ids]
    return sorted(chosen, key=lambda x: x["benefit"] - x["cost"], reverse=True)


def list_scenarios(domain: str | None = None) -> list[dict]:
    rows = read_jsonl(RUNTIME_PATHS["simulation"])
    return [r for r in rows if not domain or r.get("domain") == domain]
