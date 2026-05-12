from core.proof.audit_chain import AuditChain

def test_chain_verify():
    c=AuditChain(); c.append('import',{'id':1}); c.append('delivery',{'id':1})
    assert c.verify()
