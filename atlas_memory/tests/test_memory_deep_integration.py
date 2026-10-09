from atlas_memory.src import integration, simulation_store, social_store
from atlas_memory.src.production_readiness import run_production_check
from atlas_memory.src.anti_confusion import run_anti_confusion_scan


def test_governance_ingest_populates_simulation_and_social():
    integration.ingest_governance_health()
    assert simulation_store.list_scenarios(domain="governance")
    assert social_store.list_social_signals()


def test_social_requires_explicit_consent():
    before = len(social_store.list_social_signals())
    out = social_store.record_social_signal("client_pref", "user", "prefers sms", consent_explicit=False)
    assert out is None
    assert len(social_store.list_social_signals()) == before


def test_production_check_blocks_without_keys(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("TAVILY_API_KEY", raising=False)
    report = run_production_check(mode="production")
    assert report["ok"] is False
    assert report["reason"] == "missing_api_keys"


def test_anti_confusion_detects_ambiguous_file(tmp_path):
    bad = tmp_path / "module_final_tmp.py"
    bad.write_text("print('x')\n", encoding="utf-8")
    report = run_anti_confusion_scan(repo_root=tmp_path)
    assert report["forbidden_name_hits"] >= 1
