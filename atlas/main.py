#!/usr/bin/env python3
"""Atlas Rapporteur d’Affaires - V0.3.
Pipeline local:
1) ingestion de signaux publics démo
2) scoring simple
3) matching artisans
4) génération rapport Markdown + export JSON/CSV
"""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
RUNTIME_DIR = BASE_DIR / "runtime"
OUTPUTS_DIR = RUNTIME_DIR / "outputs"
REPORTS_DIR = RUNTIME_DIR / "reports"
EXPORT_DIR = RUNTIME_DIR / "export"

URGENCY_WEIGHTS = {"low": 1, "medium": 2, "high": 3}
CATEGORY_THRESHOLDS = [
    ("TITAN", 85),
    ("GROS", 65),
    ("MOYEN", 40),
    ("PETIT", 0),
]


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
    budget_score = min(lead.budget_eur / 120.0, 40)
    city_weight = city_weights.get(lead.city, 1.0)
    raw_score = (urgency * 20.0 + budget_score) * city_weight
    return round(min(raw_score, 100.0), 2)


def category_from_score(score: float) -> str:
    for label, threshold in CATEGORY_THRESHOLDS:
        if score >= threshold:
            return label
    return "PETIT"


def load_city_weights() -> dict[str, float]:
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
        "# Atlas Rapporteur d’Affaires — Rapport V0.3",
        "",
        f"Généré le: {now}",
        "",
        "## Top 5 des leads",
        "",
        "| Rang | ID | Ville | Métier | Score/100 | Catégorie |",
        "|---:|---|---|---|---:|---|",
    ]

    for index, lead in enumerate(scored_leads[:5], start=1):
        lines.append(
            f"| {index} | {lead['id']} | {lead['city']} | {lead['trade_hint']} | "
            f"{lead['score']} | {lead['category']} |"
        )

    lines += [
        "",
        "## Leads priorisés",
        "",
        "| ID | Ville | Métier | Budget (€) | Urgence | Score/100 | Catégorie | Artisan recommandé |",
        "|---|---|---|---:|---|---:|---|---|",
    ]

    for lead in scored_leads:
        artisan_name = lead["matched_artisan"]["name"] if lead["matched_artisan"] else "Aucun"
        lines.append(
            f"| {lead['id']} | {lead['city']} | {lead['trade_hint']} | {lead['budget_eur']} | "
            f"{lead['urgency']} | {lead['score']} | {lead['category']} | {artisan_name} |"
        )

    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def export_csv(scored_leads: list[dict[str, Any]], output_path: Path) -> None:
    fieldnames = [
        "id", "title", "city", "zip_code", "trade_hint", "budget_eur", "urgency",
        "source", "score", "category", "matched_artisan_name", "matched_artisan_id",
    ]
    with output_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        for lead in scored_leads:
            artisan = lead.get("matched_artisan") or {}
            writer.writerow({
                "id": lead["id"],
                "title": lead["title"],
                "city": lead["city"],
                "zip_code": lead["zip_code"],
                "trade_hint": lead["trade_hint"],
                "budget_eur": lead["budget_eur"],
                "urgency": lead["urgency"],
                "source": lead["source"],
                "score": lead["score"],
                "category": lead["category"],
                "matched_artisan_name": artisan.get("name", ""),
                "matched_artisan_id": artisan.get("artisan_id", ""),
            })


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
        lead_dict["category"] = category_from_score(lead_dict["score"])
        scored.append(lead_dict)

    scored.sort(key=lambda x: x["score"], reverse=True)
    matched = match_artisans(scored, artisans)

    report_path = REPORTS_DIR / "lead_report.md"
    export_path = EXPORT_DIR / "leads_ranked.json"
    export_csv_path = EXPORT_DIR / "leads_ranked.csv"

    generate_markdown_report(matched, report_path)
    export_path.write_text(json.dumps(matched, ensure_ascii=False, indent=2), encoding="utf-8")
    export_csv(matched, export_csv_path)

    summary = {
        "status": "ok",
        "leads_processed": len(matched),
        "report": str(report_path),
        "export": str(export_path),
        "export_csv": str(export_csv_path),
    }
    (OUTPUTS_DIR / "run_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary


if __name__ == "__main__":
    result = run_pipeline()
    print(json.dumps(result, indent=2, ensure_ascii=False))
