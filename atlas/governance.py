from __future__ import annotations
from atlas.models import QUALIFICATION_BUSINESS_READY, REALITY_COLLECTED, REALITY_DEMO, REALITY_HUMAN_CONFIRMED

FORBIDDEN_DEMO_DOMAINS = ("example.org", "example.local", "example.com")


def validate_no_fake_real_data(leads: list[dict], artisans: list[dict], crm_actions: list[dict] | None = None) -> list[str]:
    errors: list[str] = []
    crm_actions = crm_actions or []
    confirmed_ids = {x.get("lead_id") for x in crm_actions if x.get("action") == "HUMAN_CONFIRMED"}

    for lead in leads:
        url = (lead.get("source_url") or "").lower()
        if lead.get("qualification_status") == QUALIFICATION_BUSINESS_READY and lead.get("reality_status") == REALITY_DEMO:
            errors.append(f"DEMO en BUSINESS_READY: {lead.get('lead_id')}")
        if any(d in url for d in FORBIDDEN_DEMO_DOMAINS) and lead.get("qualification_status") == QUALIFICATION_BUSINESS_READY:
            errors.append(f"Domaine fictif en BUSINESS_READY: {lead.get('lead_id')}")
        if lead.get("reality_status") == REALITY_COLLECTED and not lead.get("source_url"):
            errors.append(f"Lead COLLECTED_FROM_URL sans URL: {lead.get('lead_id')}")
        if lead.get("reality_status") == REALITY_HUMAN_CONFIRMED and lead.get("lead_id") not in confirmed_ids:
            errors.append(f"HUMAN_CONFIRMED sans action CRM: {lead.get('lead_id')}")

    for artisan in artisans:
        if artisan.get("source_kind") == REALITY_DEMO and artisan.get("recommended_as_real"):
            errors.append(f"Artisan DEMO recommandé réel: {artisan.get('name')}")

    return errors
