from core.readiness.scoring import readiness_score

def test_saas_readiness_honest():
    r=readiness_score({'pilot_ready':True,'Multi-tenant isolation':8,'Tenant-aware RBAC':8,'Scale architecture':5})
    assert r['multi_tenant_pilot_ready'] is True
    assert r['public_saas_ready'] is False
    assert r['scale_100m']=='architecture foundation only'
