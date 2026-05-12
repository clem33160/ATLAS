def readiness_score(evidence: dict) -> dict:
    categories = ['Connectors','Documents','Security','User rights','OCR','Audit','Artisan product','Dashboard','Sales value','Reliability','RGPD readiness','Multi-client readiness','Multi-tenant isolation','Tenant-aware RBAC','Tenant-aware connectors','Backup/restore','Privacy/RGPD workflows','Billing/quotas','Observability','Scale architecture']
    scores = {c: evidence.get(c,0) for c in categories}
    avg = sum(scores.values())/len(categories)
    multi_tenant_pilot = scores['Multi-tenant isolation'] >= 7 and scores['Tenant-aware RBAC'] >= 7
    return {'score_10': round(avg,2), 'evidence': scores, 'blockers':[k for k,v in scores.items() if v<7], 'next_actions':'Address blockers before public SaaS claims.','pilot_ready':evidence.get('pilot_ready',False),'multi_tenant_pilot_ready':multi_tenant_pilot,'public_saas_ready':False,'scale_100m':'architecture foundation only' if scores['Scale architecture']>=1 else 'NO'}
