from functools import lru_cache

from core.proof.proof100000_clients import format_proof100000_clients_report, run_proof100000_clients


@lru_cache(maxsize=1)
def _result():
    return run_proof100000_clients('~/atlas_data/sandbox/proof100000_clients')


def test_proof100000_counts():
    r = _result()
    assert r.tenants == 100000
    assert r.users == 500000
    assert r.documents == 5000000


def test_proof100000_cross_tenant_refusal():
    assert _result().tenant_isolation_pass is True


def test_proof100000_delivery_receipts():
    assert _result().delivery_pass is True


def test_proof100000_access_control():
    assert _result().access_control_pass is True


def test_proof100000_audit_backup_usage():
    r = _result()
    assert r.audit_pass is True
    assert r.backup_manifest_pass is True
    assert r.usage_quota_pass is True


def test_proof100000_critical_fail_zero():
    assert _result().critical_fail == 0


def test_cli_proof100000_clients_output():
    out = format_proof100000_clients_report(_result())
    assert 'ATLAS PROOF100000 CLIENTS' in out
    assert 'CRITICAL_FAIL: 0' in out


def test_proof100000_runtime_is_bounded_enough():
    assert _result().timings['total_runtime'] < 30
