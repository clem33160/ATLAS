def readiness_score(evidence: dict) -> dict:
    categories = ['Connectors','Documents','Security','User rights','OCR','Audit','Artisan product','Dashboard','Sales value','Reliability','RGPD readiness','Multi-client readiness']
    scores = {c: evidence.get(c,0) for c in categories}
    avg = sum(scores.values())/len(categories)
    return {'score_10': round(avg,2), 'evidence': scores, 'blockers':[k for k,v in scores.items() if v<7], 'next_actions':'Address blockers before public SaaS claims.'}
