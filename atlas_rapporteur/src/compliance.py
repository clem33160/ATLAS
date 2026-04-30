BAD = ["annuaire", "blog", "emploi", "formation", "stage", "publicité", "artisan"]
GOOD = ["cherche", "besoin", "devis", "urgent", "urgence", "panne", "fuite", "travaux"]


def _text(lead):
    return f"{lead.title} {lead.snippet}".lower()


def is_false_lead(lead):
    txt = _text(lead)
    if lead.url.lower().endswith(".pdf") and len(lead.snippet.strip()) < 20:
        lead.rejection_reasons.append("pdf brut illisible")
        return True
    return any(x in txt for x in BAD)


def has_real_intent(lead):
    return any(x in _text(lead) for x in GOOD)


def is_potential_lead(lead):
    if not lead.url or not lead.title.strip() or not lead.snippet.strip():
        lead.rejection_reasons.append("informations incomplètes")
        return False
    if getattr(lead, "freshness_days", 3) > 15:
        lead.rejection_reasons.append("trop ancien")
        return False
    if lead.city == "INCERTAIN":
        lead.rejection_reasons.append("ville absente")
        return False
    if lead.trade == "INCERTAIN":
        lead.rejection_reasons.append("métier absent")
        return False
    if is_false_lead(lead):
        lead.rejection_reasons.append("faux lead")
        return False
    if not has_real_intent(lead):
        lead.rejection_reasons.append("intention faible")
        return False
    return True
