from atlas_memory.src import integration, simulation_store, uncertainty_store, conflict_store, causal_store, social_store
from atlas_memory.src.common import RUNTIME_PATHS, read_jsonl, write_json
from atlas_memory.src.production_readiness import run_production_check
from atlas_memory.src.anti_confusion import run_anti_confusion_scan


def test_rapporteur_ingest_populates_semantic_uncertainty_and_causal(tmp_path, monkeypatch):
    monkeypatch.setenv("ATLAS_MEMORY_RUNTIME_DIR", str(tmp_path / "runtime"))
    from atlas_memory.src.common import ensure_runtime_structure
    ensure_runtime_structure()

    leads = [{"title": "Plombier urgent Lyon", "snippet": "Client cherche plombier à Lyon en urgence", "qualification_status": "TO_VALIDATE", "url": "https://real.example/a"}, {"title": "Electricien Lyon", "snippet": "Client cherche électricien à Lyon", "qualification_status": "TO_VALIDATE", "url": "https://real.example/b"}]
    rejected = [{"title": "Lead douteux", "reason": "LOW_CONFIDENCE"}]
    summary = {"mode": "dry-run", "results_retrieved": 1}
    lp, rp, sp = tmp_path / "leads.json", tmp_path / "rej.json", tmp_path / "sum.json"
    write_json(lp, leads)
    write_json(rp, rejected)
    write_json(sp, summary)

    res = integration.ingest_rapporteur_run(summary_path=sp, rejected_path=rp, leads_path=lp)
    assert res["summary"] == "ingested"
    assert read_jsonl(RUNTIME_PATHS["semantic"])
    assert uncertainty_store.list_uncertainties()
    assert causal_store.list_causal_links()  # runtime non vide


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
