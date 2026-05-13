from functools import lru_cache
import subprocess

from core.proof.proof_quadrillion_clients import (
    format_proof_quadrillion_clients_report,
    run_proof_quadrillion_clients,
    synthetic_document_for,
)


@lru_cache(maxsize=1)
def _result():
    return run_proof_quadrillion_clients()


def test_quadrillion_counts_are_exact():
    r = _result()
    assert r.total_clients == 1_000_000_000_000_000
    assert r.total_entities == 1_000_000_000_000_000
    assert r.total_users == 5_000_000_000_000_000
    assert r.total_documents == 100_000_000_000_000_000


def test_quadrillion_uses_big_ints():
    r = _result()
    assert isinstance(r.total_documents, int)
    assert r.total_documents > 2**53


def test_quadrillion_does_not_generate_massive_files():
    r = _result()
    assert r.physical_generation == "NO"
    assert r.model_type == "theoretical architecture stress model only"


def test_quadrillion_synthetic_document_generation():
    doc = synthetic_document_for(999_999_999_999_999, 99)
    assert doc["tenant_id"].startswith("CL-")
    assert "DOC-099" in doc["document_id"]
    assert doc["checksum"]


def test_quadrillion_shard_partition_positive():
    r = _result()
    assert r.estimated_shards > 0
    assert r.estimated_partitions > 0


def test_quadrillion_cross_tenant_refusal_sampled():
    r = _result()
    assert r.cross_tenant_refusals_sampled == 100_000
    assert r.search_samples == 100_000
    assert r.delivery_samples == 100_000
    assert r.rbac_samples == 100_000
    assert r.audit_chain_samples == 10_000
    assert r.backup_manifest_samples == 10_000


def test_quadrillion_no_false_production_claim():
    r = _result()
    assert r.production_ready == "NO"
    assert "theoretical architecture stress model only" == r.model_type


def test_cli_proof_quadrillion_clients_output():
    out = subprocess.check_output(["bash", "scripts/atlas", "proof-quadrillion-clients"], text=True)
    assert "ATLAS PROOF QUADRILLION CLIENTS" in out
    assert "CRITICAL_FAIL: 0" in out
    assert "Production-ready: NO" in out


def test_format_report_contains_required_decision():
    out = format_proof_quadrillion_clients_report(_result())
    assert "Decision: PROOF_QUADRILLION_CLIENTS_ARCHITECTURE_PASS" in out
