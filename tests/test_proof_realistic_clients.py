from core.cli_reports import readiness_report
from core.proof.proof_realistic_clients import format_proof_realistic_clients_report, run_proof_realistic_clients


def _result():
    return run_proof_realistic_clients('~/atlas_data/sandbox/proof_realistic_clients')


def test_realistic_documents_created():
    r = _result()
    assert len(r.documents) >= 500


def test_realistic_classification():
    r = _result()
    assert r.checks['documents']


def test_realistic_human_unique_request():
    r = _result()
    assert any(req['expected_status'] == 'unique' for req in r.human_requests)


def test_realistic_human_ambiguous_request():
    r = _result()
    assert any(req['expected_status'] == 'ambiguous' for req in r.human_requests)


def test_realistic_access_denial():
    r = _result()
    assert r.checks['access_control']


def test_realistic_sha_modified_refusal():
    r = _result()
    assert r.checks['sha_refusal']


def test_realistic_sensitive_documents_protected():
    r = _result()
    assert r.checks['sensitive_protection']


def test_realistic_ugly_scan_goes_to_verify_or_extracts_clues():
    r = _result()
    assert r.checks['ugly_scans']


def test_cli_proof_realistic_clients_output():
    out = format_proof_realistic_clients_report(_result())
    assert 'ATLAS PROOF REALISTIC CLIENTS' in out
    assert 'Decision: PROOF_REALISTIC_CLIENTS_PASS' in out


def test_no_false_production_claim():
    out = format_proof_realistic_clients_report(_result())
    assert 'Production-ready: NO' in out
    assert 'Public SaaS-ready: NO' in out
    readiness = readiness_report()
    assert 'Production-ready: NO' in readiness
    assert 'Public SaaS-ready: NO' in readiness
