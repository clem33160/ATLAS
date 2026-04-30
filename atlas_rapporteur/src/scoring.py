def score_lead(lead):
    s=0
    s += 15 if lead.urgency=='URGENT' else 7
    s += max(0,15-min(lead.freshness_days,15))
    s += 12 if 'devis' in (lead.snippet+lead.title).lower() else 8
    s += 20 if lead.trade in ['rénovation complète','toiture','pompe à chaleur','chaudière'] else 12
    s += 10 if lead.trade!='INCERTAIN' else 0
    s += 5 if lead.city!='INCERTAIN' else 0
    contact = sum(1 for c in [lead.contact_phone,lead.contact_email,lead.contact_form] if c!='ABSENT')
    s += min(10,contact*4)
    s += 5 if lead.url.startswith('http') else 0
    s += 5 if contact>0 and lead.freshness_days<=5 else 2
    lead.score=min(100,s)
    lead.tier='TITAN' if lead.score>=85 else 'GROS' if lead.score>=70 else 'MOYEN' if lead.score>=55 else 'PETIT' if lead.score>=40 else 'REJETE'
    return lead
