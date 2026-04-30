BAD=["blog","wikipedia","formation","emploi","annuaire","comparateur"]
GOOD=["cherche","besoin","devis","urgent","panne","fuite","travaux"]

def is_false_lead(lead):
    text=f"{lead.title} {lead.snippet}".lower()
    return any(x in text for x in BAD)

def has_real_intent(lead):
    text=f"{lead.title} {lead.snippet}".lower()
    return any(x in text for x in GOOD)

def is_potential_lead(lead):
    if getattr(lead, "freshness_days", 3)>15:
        lead.rejection_reasons.append('trop ancien')
        return False
    if is_false_lead(lead):
        lead.rejection_reasons.append('faux lead')
        return False
    if not has_real_intent(lead):
        lead.rejection_reasons.append('intention faible')
        return False
    return True
