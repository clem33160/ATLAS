from core.proof.proof100_clients import run_proof100_clients


def test_proof100_clients():
    result = run_proof100_clients('~/atlas_data/sandbox/proof100_clients')
    assert result.tenants == 100
    assert result.users == 500
    assert result.documents == 5000
    assert result.tenant_isolation_pass is True
    assert result.delivery_pass is True
    assert result.access_control_pass is True
    assert result.audit_pass is True
    assert result.backup_manifest_pass is True
    assert result.critical_fail == 0
