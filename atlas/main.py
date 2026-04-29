#!/usr/bin/env python3
"""Atlas Rapporteur d’Affaires - V0.5."""

from __future__ import annotations

import csv
import json
import re
import unicodedata
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
INBOX_DIR = BASE_DIR / "inbox"
RUNTIME_DIR = BASE_DIR / "runtime"
OUTPUTS_DIR = RUNTIME_DIR / "outputs"
REPORTS_DIR = RUNTIME_DIR / "reports"
EXPORT_DIR = RUNTIME_DIR / "export"

URGENCY_NORMALIZATION = {
    "low": "low", "basse": "low", "faible": "low",
    "medium": "medium", "moyenne": "medium", "normal": "medium",
    "high": "high", "haute": "high", "urgent": "high", "élevée": "high",
}
STATUS_NEW = "NOUVEAU"
PIPELINE_STATUSES = {"NOUVEAU", "À_APPELER", "APPELÉ", "INTÉRESSÉ", "À_RELANCER", "DEAL_POTENTIEL", "SIGNÉ", "PERDU"}
RENTABLE_TRADES = {"rénovation", "toiture", "chauffage"}
TRADES_ALIASES = {"electricite": "électricité", "elec": "électricité", "renovation": "rénovation"}

CATEGORY_THRESHOLDS = [("TITAN", 85), ("GROS", 65), ("MOYEN", 40), ("PETIT", 0)]
SOURCE_SCORE = {
    "annonce_demo": 9,
    "plateforme_locale_demo": 8,
    "annuaire_demo": 7,
    "groupe_voisinage_demo": 6,
    "forum_local_demo": 5,
    "inbox_manual": 7,
}


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
    confidence: float = 0.6
    pipeline_status: str = STATUS_NEW


def strip_accents(value: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFKD", value) if not unicodedata.combining(c))


def normalize_city(city: str) -> str:
    cleaned = strip_accents((city or "").strip().lower())
    mapping = {"lyon": "Lyon", "marseille": "Marseille", "toulouse": "Toulouse"}
    return mapping.get(cleaned, (city or "Inconnue").strip().title())


def normalize_trade(trade: str) -> str:
    cleaned = strip_accents((trade or "").strip().lower())
    cleaned = TRADES_ALIASES.get(cleaned, cleaned)
    return "électricité" if cleaned == "electricite" else cleaned


def parse_budget(value: Any) -> int:
    if isinstance(value, (int, float)):
        return max(0, int(value))
    text = re.sub(r"[^0-9]", "", str(value or ""))
    return int(text) if text else 0


def normalize_urgency(value: str) -> str:
    return URGENCY_NORMALIZATION.get(strip_accents((value or "").strip().lower()), "medium")


def normalize_confidence(value: Any) -> float:
    try:
        score = float(value)
    except (TypeError, ValueError):
        score = 0.5
    return max(0.0, min(score, 1.0))


def load_json(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def load_csv(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def normalize_lead(raw: dict[str, Any], index: int, source_file: str = "") -> dict[str, Any]:
    title = str(raw.get("title", "")).strip() or f"Lead manuel {index}"
    normalized = {
        "id": str(raw.get("id") or f"inbox-{index:03d}"),
        "title": title,
        "description": str(raw.get("description", "")).strip(),
        "city": normalize_city(str(raw.get("city", ""))),
        "zip_code": str(raw.get("zip_code", "")).strip(),
        "trade_hint": normalize_trade(str(raw.get("trade_hint", ""))),
        "budget_eur": parse_budget(raw.get("budget_eur")),
        "urgency": normalize_urgency(str(raw.get("urgency", ""))),
        "source": str(raw.get("source") or ("inbox_manual" if source_file else "unknown")),
        "confidence": normalize_confidence(raw.get("confidence", 0.6)),
        "pipeline_status": str(raw.get("pipeline_status") or STATUS_NEW),
    }
    if normalized["pipeline_status"] not in PIPELINE_STATUSES:
        normalized["pipeline_status"] = STATUS_NEW
    return normalized


def ingest_sources() -> list[dict[str, Any]]:
    all_raw = load_json(DATA_DIR / "sources" / "demo_public_signals.json")
    for inbox_file in sorted(INBOX_DIR.glob("*.json")):
        all_raw.extend(load_json(inbox_file))
    for inbox_file in sorted(INBOX_DIR.glob("*.csv")):
        all_raw.extend(load_csv(inbox_file))
    return [normalize_lead(item, idx + 1) for idx, item in enumerate(all_raw)]


def deduplicate_leads(leads: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    uniques: list[dict[str, Any]] = []
    duplicates: list[dict[str, Any]] = []
    for lead in leads:
        dup = None
        for seen in uniques:
            similar_title = (set(strip_accents(lead["title"].lower()).split()) & set(strip_accents(seen["title"].lower()).split()))
            budget_close = abs(lead["budget_eur"] - seen["budget_eur"]) <= 500
            if lead["city"] == seen["city"] and lead["trade_hint"] == seen["trade_hint"] and len(similar_title) >= 2 and budget_close:
                dup = seen
                break
        if dup:
            duplicates.append({"duplicate_id": lead["id"], "original_id": dup["id"], "city": lead["city"], "trade_hint": lead["trade_hint"]})
        else:
            uniques.append(lead)
    return uniques, duplicates


def score_lead(lead: dict[str, Any], city_weights: dict[str, float], artisans: list[dict[str, Any]]) -> float:
    budget = min((lead["budget_eur"] / 20000.0) * 25.0, 25.0)
    urgency = {"low": 7.0, "medium": 13.0, "high": 20.0}.get(lead["urgency"], 10.0)
    clarity = min((len(lead["title"]) + len(lead["description"])) / 18.0, 15.0)
    rentable = 15.0 if lead["trade_hint"] in RENTABLE_TRADES else 8.0
    source = SOURCE_SCORE.get(lead["source"], 5)
    has_match = any(a["trade"] == lead["trade_hint"] and lead["city"] in a["cities"] and a["capacity"] > 0 for a in artisans)
    matching = 10.0 if has_match else 2.0
    confidence = lead["confidence"] * 5.0
    city_boost = city_weights.get(lead["city"], 1.0)
    total = (budget + urgency + clarity + rentable + source + matching + confidence) * city_boost
    return round(min(100.0, total), 2)


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
        compatible = [a for a in artisans if a["trade"] == lead["trade_hint"] and lead["city"] in a["cities"] and a["capacity"] > 0]
        compatible.sort(key=lambda a: (a["quality_score"], a["capacity"]), reverse=True)
        selected = compatible[0] if compatible else None
        copy = dict(lead)
        copy["matched_artisan"] = selected
        enriched.append(copy)
    return enriched


def generate_markdown_report(scored_leads: list[dict[str, Any]], duplicates: list[dict[str, Any]], output_path: Path) -> None:
    now = datetime.now(timezone.utc).isoformat()
    by_city: dict[str, int] = {}
    by_trade: dict[str, int] = {}
    by_cat: dict[str, int] = {}
    missing = 0
    for lead in scored_leads:
        by_city[lead["city"]] = by_city.get(lead["city"], 0) + 1
        by_trade[lead["trade_hint"]] = by_trade.get(lead["trade_hint"], 0) + 1
        by_cat[lead["category"]] = by_cat.get(lead["category"], 0) + 1
        if not lead["description"] or not lead["zip_code"]:
            missing += 1

    lines = ["# Atlas Rapporteur d’Affaires — Rapport V0.5", "", f"Généré le: {now}", "", "## Résumé exécutif", f"- Leads retenus: {len(scored_leads)}", f"- Doublons détectés: {len(duplicates)}", f"- Champs incomplets: {missing}", "", "## Top 10 leads", "", "| Rang | ID | Ville | Métier | Score | Catégorie | Statut |", "|---:|---|---|---|---:|---|---|"]
    for idx, lead in enumerate(scored_leads[:10], start=1):
        lines.append(f"| {idx} | {lead['id']} | {lead['city']} | {lead['trade_hint']} | {lead['score']} | {lead['category']} | {lead['pipeline_status']} |")
    lines += ["", "## Totaux par ville"] + [f"- {k}: {v}" for k, v in sorted(by_city.items())]
    lines += ["", "## Totaux par métier"] + [f"- {k}: {v}" for k, v in sorted(by_trade.items())]
    lines += ["", "## Totaux par catégorie"] + [f"- {k}: {v}" for k, v in sorted(by_cat.items())]
    lines += ["", "## Doublons détectés"] + ([f"- {d['duplicate_id']} ~ {d['original_id']} ({d['city']}/{d['trade_hint']})" for d in duplicates] or ["- Aucun"]) 
    lines += ["", "## Leads à appeler en priorité"]
    for lead in [l for l in scored_leads if l["pipeline_status"] in {"NOUVEAU", "À_APPELER"}][:5]:
        lines.append(f"- {lead['id']} ({lead['title']}) score={lead['score']}")
    lines += ["", "## Artisans recommandés"]
    for lead in scored_leads[:10]:
        artisan = lead.get("matched_artisan")
        lines.append(f"- {lead['id']}: {(artisan or {}).get('name', 'Aucun')}" )
    lines += ["", "## Incertitudes / champs manquants", f"- Nombre de leads incomplets: {missing}"]
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def export_csv(scored_leads: list[dict[str, Any]], output_path: Path) -> None:
    fieldnames = ["id", "title", "description", "city", "zip_code", "trade_hint", "budget_eur", "urgency", "source", "confidence", "pipeline_status", "score", "category", "matched_artisan_name", "matched_artisan_id"]
    with output_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        for lead in scored_leads:
            artisan = lead.get("matched_artisan") or {}
            writer.writerow({**{k: lead.get(k, "") for k in fieldnames}, "matched_artisan_name": artisan.get("name", ""), "matched_artisan_id": artisan.get("artisan_id", "")})


def run_pipeline() -> dict[str, Any]:
    for d in (OUTPUTS_DIR, REPORTS_DIR, EXPORT_DIR, INBOX_DIR):
        d.mkdir(parents=True, exist_ok=True)
    city_weights = load_city_weights()
    artisans = load_json(DATA_DIR / "artisans" / "demo_artisans.json")
    raw_leads = ingest_sources()
    unique_leads, duplicates = deduplicate_leads(raw_leads)
    scored = []
    for lead in unique_leads:
        item = dict(lead)
        item["score"] = score_lead(item, city_weights, artisans)
        item["category"] = category_from_score(item["score"])
        scored.append(item)
    scored.sort(key=lambda x: x["score"], reverse=True)
    matched = match_artisans(scored, artisans)

    report_path = REPORTS_DIR / "lead_report.md"
    export_json_path = EXPORT_DIR / "leads_ranked.json"
    export_csv_path = EXPORT_DIR / "leads_ranked.csv"
    execution_summary_path = OUTPUTS_DIR / "run_summary.json"
    generate_markdown_report(matched, duplicates, report_path)
    export_json_path.write_text(json.dumps({"leads": matched, "duplicates": duplicates}, ensure_ascii=False, indent=2), encoding="utf-8")
    export_csv(matched, export_csv_path)
    summary = {"status": "ok", "version": "v0.5", "leads_processed": len(matched), "duplicates_detected": len(duplicates), "report": str(report_path), "export": str(export_json_path), "export_csv": str(export_csv_path), "execution_summary": str(execution_summary_path)}
    execution_summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    return summary


if __name__ == "__main__":
    print(json.dumps(run_pipeline(), indent=2, ensure_ascii=False))
