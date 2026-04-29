#!/usr/bin/env python3
"""Atlas Rapporteur d’Affaires - V0.6."""
from __future__ import annotations

import csv
import json
import re
import unicodedata
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
INBOX_DIR = BASE_DIR / "inbox"
RUNTIME_DIR = BASE_DIR / "runtime"
EXAMPLES_DIR = BASE_DIR / "examples"

STATUS_NEW = "NOUVEAU"
PIPELINE_STATUSES = {"NOUVEAU", "À_APPELER", "APPELÉ", "INTÉRESSÉ", "À_RELANCER", "DEAL_POTENTIEL", "SIGNÉ", "PERDU", "ARCHIVE"}
CALL_STATUSES = {"NON_APPELÉ", "APPELÉ_SANS_RÉPONSE", "CONTACTÉ", "INTÉRESSÉ", "PAS_INTÉRESSÉ", "À_RELANCER", "SIGNÉ", "PERDU"}


def strip_accents(value: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFKD", value) if not unicodedata.combining(c))


def normalize_city(city: str) -> str:
    cleaned = strip_accents((city or "").strip().lower())
    mapping = {"lyon": "Lyon", "marseille": "Marseille", "toulouse": "Toulouse", "paris": "Paris"}
    return mapping.get(cleaned, (city or "Inconnue").strip().title())


def normalize_trade(trade: str) -> str:
    cleaned = strip_accents((trade or "").strip().lower())
    aliases = {"electricite": "électricité", "elec": "électricité", "renovation": "rénovation"}
    return aliases.get(cleaned, cleaned)


def parse_budget(value: Any) -> int:
    if isinstance(value, (int, float)):
        return max(0, int(value))
    text = re.sub(r"[^0-9]", "", str(value or ""))
    return int(text) if text else 0


def load_json(path: Path) -> list[dict[str, Any]]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_csv(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def normalize_lead(raw: dict[str, Any], index: int, source_file: str = "") -> dict[str, Any]:
    missing = []
    city = normalize_city(str(raw.get("city", "")))
    trade = normalize_trade(str(raw.get("trade_hint", "")))
    if city in {"", "Inconnue"}:
        missing.append("city")
    if not trade:
        missing.append("trade_hint")

    evidence_url = str(raw.get("evidence_url") or "")
    evidence_status = "CONFIRMÉ" if evidence_url else "PARTIEL"
    confidence = float(raw.get("confidence", 0.6) or 0.6)
    if not evidence_url:
        confidence = max(0.2, confidence - 0.15)

    budget = parse_budget(raw.get("budget_eur"))
    budget_conf = "EXACT" if budget > 0 else "ESTIMÉ"
    if budget == 0:
        budget = 3000

    return {
        "id": str(raw.get("id") or f"lead-{index:03d}"),
        "title": str(raw.get("title") or f"Lead {index}").strip(),
        "description": str(raw.get("description", "")).strip(),
        "city": city,
        "zip_code": str(raw.get("zip_code", "")).strip(),
        "country": str(raw.get("country") or "FR").strip(),
        "trade_hint": trade,
        "normalized_trade": trade,
        "budget_eur": budget,
        "budget_confidence": budget_conf,
        "urgency": str(raw.get("urgency") or "medium"),
        "urgency_reason": str(raw.get("urgency_reason") or "Déduit du texte"),
        "source": str(raw.get("source") or ("inbox_manual" if source_file else "demo")),
        "source_type": str(raw.get("source_type") or "demo"),
        "evidence_url": evidence_url,
        "evidence_source_id": str(raw.get("evidence_source_id") or "manual_url"),
        "evidence_collected_at": str(raw.get("evidence_collected_at") or now_iso()),
        "evidence_raw_excerpt": str(raw.get("evidence_raw_excerpt") or raw.get("description", ""))[:180],
        "evidence_summary": str(raw.get("evidence_summary") or "Preuve à valider"),
        "evidence_confidence": round(confidence, 2),
        "evidence_status": str(raw.get("evidence_status") or evidence_status),
        "uncertainty_notes": str(raw.get("uncertainty_notes") or ("URL absente" if not evidence_url else "")),
        "confidence": round(confidence, 2),
        "pipeline_status": raw.get("pipeline_status") if raw.get("pipeline_status") in PIPELINE_STATUSES else STATUS_NEW,
        "qualification_status": "À_VALIDER" if missing else "QUALIFIÉ",
        "missing_fields": missing,
        "risk_flags": ["MISSING_FIELDS"] if missing else [],
    }


def score_lead(lead: dict[str, Any], artisans: list[dict[str, Any]]) -> tuple[int, dict[str, int]]:
    budget_score = min(25, int(lead["budget_eur"] / 1200))
    urgency_score = {"low": 5, "medium": 10, "high": 15}.get(lead["urgency"], 8)
    clarity_score = min(10, int((len(lead["title"]) + len(lead["description"])) / 28))
    evidence_score = {"ESTIMÉ": 4, "PARTIEL": 9, "CONFIRMÉ": 15, "À_VALIDER": 6}.get(lead["evidence_status"], 6)
    trade_profitability_score = 10 if lead["normalized_trade"] in {"rénovation", "toiture", "chauffage", "électricité"} else 6
    location_score = 5 if lead["city"] != "Inconnue" else 1
    artisan_match_score = 10 if any(lead["normalized_trade"] in a.get("trades", []) for a in artisans) else 2
    closing_probability_score = 5 if lead["urgency"] == "high" else 3
    confidence_score = int(max(0, min(5, round(lead["confidence"] * 5))))
    breakdown = {
        "budget_score": budget_score,
        "urgency_score": urgency_score,
        "clarity_score": clarity_score,
        "evidence_score": evidence_score,
        "trade_profitability_score": trade_profitability_score,
        "location_score": location_score,
        "artisan_match_score": artisan_match_score,
        "closing_probability_score": closing_probability_score,
        "confidence_score": confidence_score,
    }
    return sum(breakdown.values()), breakdown


def category_from_score(score: float) -> str:
    if score >= 85:
        return "TITAN"
    if score >= 70:
        return "GROS"
    if score >= 55:
        return "MOYEN"
    if score >= 40:
        return "PETIT"
    return "FAIBLE"


def ingest_sources() -> list[dict[str, Any]]:
    rows = load_json(DATA_DIR / "sources" / "demo_public_signals.json")
    for p in sorted(INBOX_DIR.glob("*.json")):
        rows.extend(load_json(p))
    for p in sorted(INBOX_DIR.glob("*.csv")):
        rows.extend(load_csv(p))
    return [normalize_lead(r, i + 1) for i, r in enumerate(rows)]


def match_artisans(leads: list[dict[str, Any]], artisans: list[dict[str, Any]]) -> list[dict[str, Any]]:
    for lead in leads:
        compatibles = [a for a in artisans if lead["normalized_trade"] in a.get("trades", []) and a.get("city") == lead["city"]]
        compatibles.sort(key=lambda x: (x.get("rating", 0), x.get("reviews_count", 0), x.get("confidence", 0)), reverse=True)
        lead["artisan_recommended"] = compatibles[0] if compatibles else {"name": "Aucun artisan fiable trouvé, validation humaine nécessaire"}
        lead["artisan_alternatives"] = compatibles[1:4]
        lead["matching_reason"] = "Métier + zone + réputation" if compatibles else "Validation humaine requise"
    return leads


def run_pipeline(mode: str = "run") -> dict[str, Any]:
    for d in [RUNTIME_DIR / "reports", RUNTIME_DIR / "export", RUNTIME_DIR / "closer", RUNTIME_DIR / "crm", RUNTIME_DIR / "matching", RUNTIME_DIR / "evidence", RUNTIME_DIR / "outputs", INBOX_DIR]:
        d.mkdir(parents=True, exist_ok=True)
    artisans = load_json(DATA_DIR / "artisans" / "demo_artisans.json")
    leads = ingest_sources()
    for lead in leads:
        lead["score"], lead["score_breakdown"] = score_lead(lead, artisans)
        lead["category"] = category_from_score(lead["score"])
        lead["qualification_status"] = "PRIORITAIRE" if lead["category"] in {"TITAN", "GROS"} else lead["qualification_status"]
    leads = sorted(match_artisans(leads, artisans), key=lambda x: x["score"], reverse=True)

    evidence_log = [{k: l[k] for k in ["id", "evidence_url", "evidence_source_id", "evidence_collected_at", "evidence_raw_excerpt", "evidence_status", "uncertainty_notes"]} for l in leads]
    (RUNTIME_DIR / "evidence" / "evidence_log.json").write_text(json.dumps(evidence_log, ensure_ascii=False, indent=2), encoding="utf-8")
    (RUNTIME_DIR / "matching" / "matches.json").write_text(json.dumps(leads, ensure_ascii=False, indent=2), encoding="utf-8")

    call_updates = load_csv(INBOX_DIR / "call_updates.csv") if (INBOX_DIR / "call_updates.csv").exists() else []
    for c in call_updates:
        if c.get("call_status") in CALL_STATUSES:
            for l in leads:
                if l["id"] == c.get("lead_id"):
                    l["pipeline_status"] = "APPELÉ" if c["call_status"] in {"CONTACTÉ", "APPELÉ_SANS_RÉPONSE"} else l["pipeline_status"]
                    l["last_action_at"] = c.get("called_at", now_iso())
                    l["next_action_at"] = c.get("next_action_at", "")
    (RUNTIME_DIR / "crm" / "call_log.json").write_text(json.dumps(call_updates, ensure_ascii=False, indent=2), encoding="utf-8")
    (RUNTIME_DIR / "crm" / "leads_history.json").write_text(json.dumps(leads, ensure_ascii=False, indent=2), encoding="utf-8")
    (RUNTIME_DIR / "crm" / "status_changes.json").write_text(json.dumps([{"lead_id": l["id"], "pipeline_status": l["pipeline_status"]} for l in leads], ensure_ascii=False, indent=2), encoding="utf-8")

    report = RUNTIME_DIR / "reports" / "lead_report.md"
    lines = ["# Atlas Rapporteur d’Affaires — Rapport V0.6", "", "## Résumé exécutif", f"- Leads traités: {len(leads)}", f"- Leads TITAN: {sum(1 for l in leads if l['category']=='TITAN')}"]
    lines += ["", "## Top 10 leads"]
    for i, l in enumerate(leads[:10], 1):
        lines.append(f"- {i}. {l['id']} | {l['city']} | {l['normalized_trade']} | {l['score']} ({l['category']})")
        lines.append(f"  - Preuve: {l['evidence_url'] or 'N/A'} | Collecte: {l['evidence_collected_at']} | Confiance: {l['evidence_confidence']}")
    lines += ["", "## Suivi appels", f"- Leads appelés: {sum(1 for l in leads if l.get('pipeline_status')=='APPELÉ')}"]
    report.write_text("\n".join(lines)+"\n", encoding="utf-8")

    export_json = RUNTIME_DIR / "export" / "leads_ranked.json"
    export_json.write_text(json.dumps({"leads": leads}, ensure_ascii=False, indent=2), encoding="utf-8")
    with (RUNTIME_DIR / "export" / "leads_ranked.csv").open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["id", "city", "normalized_trade", "score", "category", "pipeline_status", "evidence_url"])
        w.writeheader(); [w.writerow({k: l.get(k, "") for k in w.fieldnames}) for l in leads]

    closer_md = RUNTIME_DIR / "closer" / "daily_call_sheet.md"
    closer_lines = ["# Daily Call Sheet", "", "| ordre | lead_id | ville | métier | titre | budget | score | catégorie | preuve | artisan | prochaine action |", "|---:|---|---|---|---|---:|---:|---|---|---|---|"]
    for i, l in enumerate(leads[:15], 1):
        closer_lines.append(f"| {i} | {l['id']} | {l['city']} | {l['normalized_trade']} | {l['title']} | {l['budget_eur']} | {l['score']} | {l['category']} | {(l['evidence_summary'] or '')[:40]} | {l['artisan_recommended'].get('name','')} | {l.get('next_action_at','À planifier')} |")
    closer_lines += ["", "Script d'appel: présenter Atlas, ne rien promettre, vérifier le besoin réel, demander accord avant transmission, noter consentement/refus."]
    closer_md.write_text("\n".join(closer_lines)+"\n", encoding="utf-8")
    (RUNTIME_DIR / "closer" / "priority_leads.md").write_text("\n".join([f"- {l['id']} {l['score']}" for l in leads if l['category'] in {'TITAN','GROS'}]), encoding="utf-8")
    with (RUNTIME_DIR / "closer" / "daily_call_sheet.csv").open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["order","lead_id","city","trade","title","budget","score","category"]); w.writeheader()
        for i,l in enumerate(leads[:15],1): w.writerow({"order":i,"lead_id":l["id"],"city":l["city"],"trade":l["normalized_trade"],"title":l["title"],"budget":l["budget_eur"],"score":l["score"],"category":l["category"]})

    summary = {"status":"ok","report":str(report),"export":str(export_json),"export_csv":str(RUNTIME_DIR / "export" / "leads_ranked.csv"),"execution_summary":str(RUNTIME_DIR / "outputs" / "run_summary.json"),"total":len(leads)}
    (RUNTIME_DIR / "outputs" / "run_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    return summary


if __name__ == "__main__":
    import sys
    mode = sys.argv[1] if len(sys.argv) > 1 else "run"
    s = run_pipeline(mode)
    if mode == "crm-summary":
        print("CRM summary:", s["total"])
    print("ATLAS RAPPORTEUR D’AFFAIRES — V0.6")
    print("Status: OK")
