from core.access.tenant_policies import can_access_tenant

def test_cross_tenant_denied():
    assert not can_access_tenant('owner','A','B','invoice')
    assert not can_access_tenant('secretary','A','B','invoice')
    assert not can_access_tenant('apprentice','A','B','job')

def test_external_client_and_auditor():
    assert can_access_tenant('external_client','A','A','client_doc','c1','c1')
    assert not can_access_tenant('external_client','A','A','client_doc','c1','c2')
    assert can_access_tenant('auditor','A','A','proof',auditor_tenants={'A'})
