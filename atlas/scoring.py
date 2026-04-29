from __future__ import annotations
from atlas.models import INTENT_BUSINESS, QUALIFICATION_BUSINESS_READY, QUALIFICATION_TO_VALIDATE, REALITY_COLLECTED, REALITY_DEMO, REALITY_MANUAL


def score_lead(lead: dict, has_real_artisan: bool) -> dict:
    score = 0
    score += 20 if lead.get("budget_mid", 0) >= 10000 else 10
    score += 10 if lead.get("urgency") == "high" else 5
    score += 10
    score += 10 if len(lead.get("description", "")) > 40 else 4
    score += 20 if lead.get("source_url") else 0
    score += 10 if lead.get("trade") else 0
    score += 5 if lead.get("city") else 0
    score += 10 if has_real_artisan else 0
    score += 5 if lead.get("intent_type") in INTENT_BUSINESS else 0
    caps = []
    if lead.get("reality_status") == REALITY_DEMO:
        score = min(score, 60); caps.append("DEMO max 60")
    if lead.get("reality_status") == REALITY_MANUAL and not lead.get("source_url"):
        score = min(score, 65); caps.append("MANUAL sans URL max 65")
    if lead.get("reality_status") == REALITY_COLLECTED and lead.get("intent_type") in {"GENERIC_PAGE", "UNKNOWN"}:
        score = min(score, 55); caps.append("URL générique/inconnue max 55")
    lead["score_total"] = score
    lead["score_caps_applied"] = caps
    lead["qualification_status"] = QUALIFICATION_BUSINESS_READY if all([
        lead.get("source_url"), lead.get("evidence_summary"), lead.get("city"), lead.get("trade"), lead.get("intent_type") in INTENT_BUSINESS, score >= 70, has_real_artisan
    ]) else QUALIFICATION_TO_VALIDATE
    return lead
