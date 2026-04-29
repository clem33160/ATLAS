from __future__ import annotations
from atlas.models import QUALIFICATION_BUSINESS_READY, REALITY_DEMO


def compute_business_readiness(leads: list[dict], artisans: list[dict], call_feedback_count: int = 0) -> dict:
    ready = [l for l in leads if l.get("qualification_status") == QUALIFICATION_BUSINESS_READY and l.get("reality_status") != REALITY_DEMO]
    real_artisans = [a for a in artisans if a.get("source_kind") != REALITY_DEMO and a.get("source_url")]
    only_demo = bool(leads) and all(l.get("reality_status") == REALITY_DEMO for l in leads)
    generic_only = bool(leads) and all(l.get("intent_type") in {"GENERIC_PAGE", "UNKNOWN"} for l in leads)

    score = 6.5
    if ready: score += 1.0
    if real_artisans: score += 1.0
    if call_feedback_count > 0: score += 0.5
    if any(l.get("reality_status") == "HUMAN_CONFIRMED" for l in leads): score += 1.0

    cap = 10.0
    reasons = []
    if not ready: cap = min(cap, 6.0); reasons.append("0 lead BUSINESS_READY")
    if not real_artisans: cap = min(cap, 6.0); reasons.append("0 artisan vérifiable")
    if only_demo: cap = min(cap, 4.0); reasons.append("uniquement données démo")
    if generic_only: cap = min(cap, 6.0); reasons.append("URLs génériques / intent non business")
    if call_feedback_count == 0: reasons.append("aucun retour d'appel")
    if not any(l.get("reality_status") == "HUMAN_CONFIRMED" for l in leads): reasons.append("aucun HUMAN_CONFIRMED")

    score = round(min(score, cap), 1)
    return {
        "business_readiness_score": score,
        "max_score_with_current_data": cap,
        "blocking_reasons": reasons,
        "actions": [
            "Ajouter des URLs publiques ciblées avec demande client claire",
            "Ajouter des artisans vérifiables (URL officielle)",
            "Importer des retours d'appel CRM",
            "Passer les meilleurs leads en HUMAN_CONFIRMED après validation humaine",
        ],
    }
