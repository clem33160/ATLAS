from core.proof.tenant_audit import TenantAuditChain

def test_tenant_audit_chain():
    c=TenantAuditChain(); c.append('A','tenant_created',{}); c.append('A','document_imported',{'id':1}); c.append('B','document_imported',{'id':2})
    assert c.verify_tenant('A') and c.verify_tenant('B')
