def score_lead(lead):
    txt = (lead.snippet + " " + lead.title).lower()
    details = {
        "valeur_chantier": 25 if any(k in txt for k in ["rénovation", "toiture", "chaudière"]) else 15,
        "urgence": 15 if any(k in txt for k in ["urgent", "urgence", "panne", "fuite"]) else 5,
        "fraicheur": max(0, 15 - min(lead.freshness_days, 15)),
        "clarte": 10 if len(lead.snippet) > 40 else 4,
        "preuve_source": 10 if lead.url.startswith("http") else 0,
        "domaine_rentable": 10 if lead.trade in ["chauffagiste", "toiture", "rénovation"] else 6,
        "localisation": 5 if lead.city != "INCERTAIN" else 0,
        "facilite_artisan": 5 if lead.contact_phone != "ABSENT" or lead.contact_email != "ABSENT" else 2,
        "probabilite_closing": 5 if "devis" in txt else 2,
    }
    lead.score = min(100, sum(details.values()))
    lead.qualification_reasons.append(f"score_details={details}")
    lead.tier = "TO_VALIDATE"
    return lead
