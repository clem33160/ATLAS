from core.cli_reports import readiness_report
from core.proof.proof_real_pdf_classification import (
    format_proof_real_pdf_classification_report,
    run_proof_real_pdf_classification,
)


def _result():
    return run_proof_real_pdf_classification('~/atlas_data/sandbox/proof_real_pdf_classification')


def test_real_pdf_files_created():
    r = _result()
    assert len(r.documents) == 100


def test_real_pdf_text_extraction():
    assert _result().checks['text_extraction']


def test_real_pdf_classification_facture():
    r = _result()
    assert any(d['type'] == 'facture_client' for d in r.documents)


def test_real_pdf_classification_devis():
    r = _result()
    assert any(d['type'] == 'devis' for d in r.documents)


def test_real_pdf_ambiguous_search():
    r = _result()
    assert any(s['status'] == 'ambiguous' for s in r.searches)


def test_real_pdf_unique_search():
    r = _result()
    assert any(s['status'] == 'unique' for s in r.searches)


def test_real_pdf_access_control_sensitive():
    assert _result().checks['access_control']


def test_real_pdf_sha_modified_refusal():
    r = _result()
    target = r.documents[0]
    assert r.checks['sha_refusal']
    assert target['decision'] == 'REFUS_SHA_MODIFIE'


def test_real_pdf_ugly_documents_to_verify():
    assert _result().checks['ugly']


def test_cli_proof_real_pdf_classification_output():
    out = format_proof_real_pdf_classification_report(_result())
    assert 'ATLAS PROOF REAL PDF CLASSIFICATION' in out
    assert 'Decision: PROOF_REAL_PDF_CLASSIFICATION_PASS' in out


def test_no_false_production_claim():
    out = format_proof_real_pdf_classification_report(_result())
    assert 'Production-ready: NO' in out
    assert 'Public SaaS-ready: NO' in out
    readiness = readiness_report()
    assert 'Production-ready: NO' in readiness
    assert 'Public SaaS-ready: NO' in readiness
