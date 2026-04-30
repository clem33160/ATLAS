import json
from atlas_rapporteur.src.config import BASE
from atlas_rapporteur.src.legal_source_guard import guard_lead
from atlas_rapporteur.src.provider_router import discover
from atlas_rapporteur.src.provider_registry import load_provider_registry


def test_providers_json_valid_and_min_10():
    data = load_provider_registry()
    assert isinstance(data, dict)
    assert len(data["providers"]) >= 10


def test_blocked_defaults():
    blocked = {x["provider_id"]: x for x in load_provider_registry()["blocked_or_permission_required"]}
    assert blocked["leboncoin"]["legal_status"] == "blocked_without_permission"
    assert blocked["allovoisins"]["legal_status"] == "blocked_without_permission"


def test_expected_allowed_sources():
    providers = {p["provider_id"]: p for p in load_provider_registry()["providers"]}
    assert providers["boamp_fr"]["source_type"] == "OPEN_DATA_API"
    assert providers["ted_eu"]["enabled"] is True
    assert providers["seao_qc"]["enabled"] is True
    assert providers["canadabuys"]["enabled"] is True


def test_no_lead_without_url_or_proof():
    ok, reason = guard_lead({"source_url": "", "proof_required": {}})
    assert ok is False and reason == "REJECTED_NO_SOURCE_URL"
    ok, reason = guard_lead({"source_url": "http://x", "proof_required": None})
    assert ok is False and reason == "REJECTED_NO_PROOF"


def test_business_ready_requires_human_validation():
    ok, reason = guard_lead({"source_url": "http://x", "proof_required": {"url": "http://x"}, "qualification_status": "BUSINESS_READY", "human_action_required": False})
    assert ok is False and reason == "REJECTED_NO_HUMAN_VALIDATION"


def test_router_outputs_and_logs_written():
    leads, skipped = discover("renovation", limit=5)
    assert leads
    assert all(x.get("source_url") for x in leads)
    assert (BASE / "runtime/audit/provider_run_log.jsonl").exists()
    assert (BASE / "runtime/audit/source_policy_report.md").exists()
    assert (BASE / "runtime/reports/provider_sources_report.md").exists()


def test_dedup_by_url():
    leads, _ = discover("toiture", limit=5)
    urls = [x["source_url"] for x in leads]
    assert len(urls) == len(set(urls))


def test_dry_run_offline():
    from atlas_rapporteur.src.main import run
    leads, summary = run(mode="dry-run", limit=5, with_summary=True)
    assert summary["mode"] == "dry-run"
    assert isinstance(leads, list)
