from datetime import datetime
from urllib.parse import urlparse
from .models import Lead


def extract_leads(results, pages=None):
    pages = pages or {}
    leads = []
    for idx, r in enumerate(results, start=1):
        txt = f"{r.get('title','')} {r.get('snippet','')} {pages.get(r.get('url',''), '')}"
        lead = Lead(
            lead_id=f"LEAD-{idx:05d}",
            title=r.get("title", "ABSENT") or "ABSENT",
            source_url=r.get("url", "ABSENT") or "ABSENT",
            source_domain=urlparse(r.get("url", "")).netloc or "ABSENT",
            country=r.get("country", "INCONNU") or "INCONNU",
            city=r.get("city", "INCONNU") or "INCONNU",
            trade=r.get("trade", "INCONNU") or "INCONNU",
            intent_type="PUBLIC_TENDER" if "marché public" in txt.lower() else "CLIENT_REQUEST",
            urgency="URGENT" if any(k in txt.lower() for k in ["urgence", "urgent", "fuite", "panne"]) else "NORMAL",
            freshness_days=int(r.get("freshness_days", 999) or 999),
            budget_low="ABSENT", budget_mid="ABSENT", budget_high="ABSENT", budget_status="INCONNU",
            contact_phone="ABSENT", contact_email="ABSENT", contact_form="ABSENT",
            evidence_summary=(r.get("snippet", "") or "ABSENT")[:220],
            raw_snippet=r.get("snippet", "ABSENT") or "ABSENT",
            qualification_status="TO_VALIDATE",
            created_at=datetime.utcnow().isoformat(),
        )
        leads.append(lead)
    return leads
