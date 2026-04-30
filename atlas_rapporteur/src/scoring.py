
def score_lead(lead):
    txt = f"{lead.title} {lead.raw_snippet}".lower()
    score = 0
    score += 25 if any(k in txt for k in ["rénovation", "toiture", "marché public"]) else 12
    score += 15 if lead.urgency == "URGENT" else 5
    score += max(0, 15 - min(int(lead.freshness_days), 15))
    score += 10 if len(lead.raw_snippet) >= 40 else 3
    score += 10 if lead.source_url.startswith("http") and lead.evidence_summary not in ("", "ABSENT") else 0
    score += 10 if lead.trade in ["plomberie", "chauffage", "pompe à chaleur", "toiture", "électricité", "rénovation complète"] else 5
    score += 5 if lead.city != "INCONNU" and lead.country != "INCONNU" else 0
    score += 5 if lead.contact_phone != "ABSENT" or lead.contact_email != "ABSENT" else 2
    score += 5 if any(k in txt for k in ["devis", "besoin", "appel d'offres", "marché public"]) else 2
    lead.score = max(0, min(100, int(score)))
    lead.tier = "TITAN" if lead.score >= 85 else "GROS" if lead.score >= 70 else "MOYEN" if lead.score >= 55 else "PETIT" if lead.score >= 40 else "REJET"
    lead.qualification_status = "TO_VALIDATE"
    return lead
