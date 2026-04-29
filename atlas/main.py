#!/usr/bin/env python3
"""Atlas Rapporteur d’Affaires - V0 ultra minimale.
Pipeline local:
1) ingestion de signaux publics démo
2) scoring simple
3) matching artisans
4) génération rapport Markdown + export JSON
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
OUTPUTS_DIR = BASE_DIR / "outputs"
REPORTS_DIR = BASE_DIR / "reports"
EXPORT_DIR = BASE_DIR / "export"

URGENCY_WEIGHTS = {"low": 1, "medium": 2, "high": 3}


@dataclass
class Lead:
    id: str
    title: str
    description: str
    city: str
    zip_code: str
    trade_hint: str
    budget_eur: int
    urgency: str
    source: str


def load_json(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def ingest_sources() -> list[Lead]:
    raw = load_json(DATA_DIR / "sources" / "demo_public_signals.json")
    return [Lead(**entry) for entry in raw]


def score_lead(lead: Lead, city_weights: dict[str, float]) -> float:
    urgency = URGENCY_WEIGHTS.get(lead.urgency, 1)
    budget_score = min(lead.budget_eur / 1000.0, 10)
    city_weight = city_weights.get(lead.city, 1.0)
    return round((urgency * 2.0 + budget_score) * city_weight, 2)


def load_city_weights() -> dict[str, float]:
    # Parser minimal YAML-like (suffisant pour notre fichier de config V0)
    cfg_path = BASE_DIR / "config" / "cities.yaml"
    city_weights: dict[str, float] = {}
    current_city: str | None = None
    for line in cfg_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith("- name:"):
            current_city = stripped.split(":", 1)[1].strip()
        elif stripped.startswith("priority_weight:") and current_city:
            city_weights[current_city] = float(stripped.split(":", 1)[1].strip())
    return city_weights


def match_artisans(leads_with_scores: list[dict[str, Any]], artisans: list[dict[str, Any]]) -> list[dict[str, Any]]:
    enriched: list[dict[str, Any]] = []
    for lead in leads_with_scores:
        compatible = [
            a for a in artisans
            if a["trade"] == lead["trade_hint"] and lead["city"] in a["cities"] and a["capacity"] > 0
        ]
        compatible.sort(key=lambda a: (a["quality_score"], a["capacity"]), reverse=True)
        selected = compatible[0] if compatible else None
        lead_copy = dict(lead)
        lead_copy["matched_artisan"] = selected
        enriched.append(lead_copy)
    return enriched


def generate_markdown_report(scored_leads: list[dict[str, Any]], output_path: Path) -> None:
    now = datetime.now(timezone.utc).isoformat()
    lines = [
        "# Atlas Rapporteur d’Affaires — Rapport V0",
        "",
        f"Généré le: {now}",
        "",
        "## Leads priorisés",
        "",
        "| ID | Ville | Métier | Budget (€) | Urgence | Score | Artisan recommandé |",
        "|---|---|---|---:|---|---:|---|",
    ]

    for lead in scored_leads:
        artisan_name = lead["matched_artisan"]["name"] if lead["matched_artisan"] else "Aucun"
        lines.append(
            f"| {lead['id']} | {lead['city']} | {lead['trade_hint']} | {lead['budget_eur']} | "
            f"{lead['urgency']} | {lead['score']} | {artisan_name} |"
        )

    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run_pipeline() -> dict[str, Any]:
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)

    leads = ingest_sources()
    city_weights = load_city_weights()
    artisans = load_json(DATA_DIR / "artisans" / "demo_artisans.json")

    scored = []
    for lead in leads:
        lead_dict = lead.__dict__.copy()
        lead_dict["score"] = score_lead(lead, city_weights)
        scored.append(lead_dict)

    scored.sort(key=lambda x: x["score"], reverse=True)
    matched = match_artisans(scored, artisans)

    report_path = REPORTS_DIR / "lead_report.md"
    export_path = EXPORT_DIR / "leads_ranked.json"

    generate_markdown_report(matched, report_path)
    export_path.write_text(json.dumps(matched, ensure_ascii=False, indent=2), encoding="utf-8")

    summary = {
        "status": "ok",
        "leads_processed": len(matched),
        "report": str(report_path),
        "export": str(export_path),
    }
    (OUTPUTS_DIR / "run_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary


if __name__ == "__main__":
    result = run_pipeline()
    print(json.dumps(result, indent=2, ensure_ascii=False))
