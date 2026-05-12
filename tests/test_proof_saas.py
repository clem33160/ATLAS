from core.proof.proof_saas import run_proof_saas

def test_proof_saas(tmp_path):
    r=run_proof_saas(tmp_path)
    assert r['blocked_cross_tenant_delivery']
    assert r['audit_A'] and r['audit_B']
    assert r['usage_A']==1
    assert r['snapshot']['tenant_id']=='A'
    assert r['privacy_export']['type']=='export_requested'
    assert r['public_saas_ready'] is False
