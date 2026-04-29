#!/usr/bin/env python3
from __future__ import annotations
import json
from datetime import datetime, timezone
from pathlib import Path

from atlas.artisans import resolve_artisans
from atlas.business.readiness import compute_business_readiness
from atlas.closer.call_sheet import build_daily_call_sheet
from atlas.extraction import extract_signals
from atlas.governance import validate_no_fake_real_data
from atlas.models import REALITY_DEMO, REALITY_PARTIAL
from atlas.reports.lead_report import build_lead_report
from atlas.scoring import score_lead
from atlas.sources.http_fetcher import extract_text_from_html, fetch_public_url, normalize_web_text, safe_excerpt
from atlas.storage import ensure_runtime_dirs, write_csv, write_json, write_markdown

BASE = Path(__file__).resolve().parent
INBOX = BASE / "inbox"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def is_demo_url(url: str) -> bool:
    return "example." in (url or "").lower()


def parse_source_urls() -> list[dict]:
    items = []
    seen = set()
    source_path = INBOX / "source_urls.txt"
    if not source_path.exists():
        return items
    for line in source_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split("|")
        row = {"source_id": "manual", "url": parts[0], "note": ""}
        if len(parts) > 1:
            row = {"source_id": parts[0], "url": parts[1], "note": parts[2] if len(parts) > 2 else ""}
        if row["url"] not in seen:
            seen.add(row["url"])
            items.append(row)
    return items


def run_pipeline(mode: str = "run") -> dict:
    paths = ensure_runtime_dirs(BASE)
    artisans, artisan_warnings = resolve_artisans(BASE)
    leads = []
    cards = []
    errors = []

    for src in parse_source_urls():
        res = fetch_public_url(src["url"])
        if not res["ok"]:
            errors.append({"url": src["url"], "error": res.get("error", "fetch_error")})
            continue
        text = normalize_web_text(extract_text_from_html(res["raw_html"]))
        sig = extract_signals(text)
        reality = REALITY_DEMO if is_demo_url(src["url"]) else "COLLECTED_FROM_URL"
        if sig.get("city") and sig.get("trade") and reality != REALITY_DEMO:
            reality = REALITY_PARTIAL
        cards.append({"url": src["url"], "collected_at": now(), "detected_city": sig.get("city", ""), "detected_trade": sig.get("trade", "")})
        leads.append({
            "lead_id": f"url-{len(leads)+1}", "title": f"Lead {sig.get('trade') or 'à qualifier'}", "description": safe_excerpt(text, 220),
            "city": sig.get("city", ""), "trade": sig.get("trade", ""), "intent_type": sig.get("intent_type", "UNKNOWN"),
            "reality_status": reality, "source_id": src["source_id"], "source_url": src["url"], "collected_at": now(),
            "evidence_summary": safe_excerpt(text, 90), "budget_mid": sig.get("budget_mid", 0), "urgency": sig.get("urgency"), "pipeline_status": "NEW",
        })

    has_real_artisan = any(a.get("source_kind") != REALITY_DEMO and a.get("source_url") for a in artisans)
    for lead in leads:
        score_lead(lead, has_real_artisan=has_real_artisan)

    governance_warnings = validate_no_fake_real_data(leads, artisans, crm_actions=[])
    readiness = compute_business_readiness(leads, artisans, call_feedback_count=0)
    ready = [l for l in leads if l.get("qualification_status") == "BUSINESS_READY" and l.get("reality_status") != REALITY_DEMO]

    lead_report = build_lead_report(len(leads), len(ready), governance_warnings)
    call_sheet_md, call_sheet_rows = build_daily_call_sheet(leads, artisans)
    readiness_md = "# Business Readiness\n\n" + f"Score actuel: {readiness['business_readiness_score']}/10\n" + f"Plafond actuel: {readiness['max_score_with_current_data']}/10\n\n## Pourquoi pas 10/10\n" + "\n".join([f"- {x}" for x in readiness["blocking_reasons"]]) + "\n\n## Actions\n" + "\n".join([f"- {x}" for x in readiness["actions"]])

    write_json(paths["export"] / "leads_ranked.json", {"leads": leads})
    write_json(paths["evidence"] / "url_evidence_cards.json", cards)
    write_json(paths["evidence"] / "source_fetch_errors.json", errors)
    write_json(paths["business"] / "business_readiness.json", readiness)
    write_markdown(paths["business"] / "business_readiness.md", readiness_md)
    write_markdown(paths["reports"] / "lead_report.md", lead_report)
    write_markdown(paths["closer"] / "daily_call_sheet.md", call_sheet_md)
    write_csv(paths["closer"] / "daily_call_sheet.csv", call_sheet_rows, ["segment", "lead_id"])
    write_json(paths["crm"] / "pipeline_summary.json", {"to_call": len(ready), "to_validate": len(leads) - len(ready)})
    write_markdown(paths["crm"] / "call_outcomes_summary.md", "Aucun appel réel confirmé.")
    write_json(paths["artisans"] / "artisans_ranked.json", {"artisans": artisans, "warnings": artisan_warnings})
    return {"status": "ok", "mode": mode}


if __name__ == "__main__":
    run_pipeline()
    print("ATLAS RAPPORTEUR D’AFFAIRES — V0.10")
