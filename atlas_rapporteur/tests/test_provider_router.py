import io
import json
from pathlib import Path

from atlas_rapporteur.src.main import run
from atlas_rapporteur.src.provider_router import discover
from atlas_rapporteur.src.providers.brave_search import BraveSearchProvider
from atlas_rapporteur.src.providers.tavily_search import TavilySearchProvider


def test_aucun_provider_actif_ne_retourne_example_com(monkeypatch):
    monkeypatch.setenv("BRAVE_SEARCH_API_KEY", "x")
    monkeypatch.setenv("TAVILY_API_KEY", "x")
    monkeypatch.setattr(BraveSearchProvider, "search", lambda *_a, **_k: [{"url": "https://example.com/bad"}, {"url": "https://real.tld/ok", "title": "ok", "snippet": "ok"}])
    monkeypatch.setattr(TavilySearchProvider, "search", lambda *_a, **_k: [{"url": "https://example.com/xx"}])
    rows, _ = discover("q", selected="all")
    assert rows and all("example.com" not in r["url"] for r in rows)


def test_brave_sans_cle_skip_propre(monkeypatch):
    monkeypatch.delenv("BRAVE_SEARCH_API_KEY", raising=False)
    _, skipped = discover("q", selected="brave")
    assert any(s["status"] == "SKIPPED_NO_API_KEY" for s in skipped)


def test_tavily_sans_cle_skip_propre(monkeypatch):
    monkeypatch.delenv("TAVILY_API_KEY", raising=False)
    _, skipped = discover("q", selected="tavily")
    assert any(s["status"] == "SKIPPED_NO_API_KEY" for s in skipped)


def test_brave_mock_http_parse(monkeypatch):
    monkeypatch.setenv("BRAVE_SEARCH_API_KEY", "x")
    payload = json.dumps({"web": {"results": [{"title": "AO Plomberie", "url": "https://public.fr/a", "description": "besoin plombier"}]}}).encode()
    class Resp:
        def __enter__(self): return self
        def __exit__(self, *a): return False
        def read(self): return payload
    monkeypatch.setattr("urllib.request.urlopen", lambda *a, **k: Resp())
    rows = BraveSearchProvider().search("plombier", limit=5)
    assert rows and rows[0]["title"] == "AO Plomberie"


def test_tavily_mock_http_parse(monkeypatch):
    monkeypatch.setenv("TAVILY_API_KEY", "x")
    payload = json.dumps({"results": [{"title": "Marché peinture", "url": "https://public.ca/b", "content": "travaux peinture"}]}).encode()
    class Resp:
        def __enter__(self): return self
        def __exit__(self, *a): return False
        def read(self): return payload
    monkeypatch.setattr("urllib.request.urlopen", lambda *a, **k: Resp())
    rows = TavilySearchProvider().search("peinture", limit=5)
    assert rows and rows[0]["snippet"] == "travaux peinture"


def test_boamp_disabled_par_defaut():
    cfg = json.loads(Path("atlas_rapporteur/config/providers.json").read_text(encoding="utf-8"))
    assert cfg["boamp"]["enabled"] is False


def test_provider_router_ignore_disabled_et_ecrit_audit(monkeypatch):
    monkeypatch.setenv("BRAVE_SEARCH_API_KEY", "x")
    monkeypatch.setattr(BraveSearchProvider, "search", lambda *_a, **_k: [{"url": "https://ok.fr/1", "title": "t", "snippet": "s"}])
    discover("q", selected="all")
    skipped = json.loads(Path("atlas_rapporteur/runtime/audit/skipped_providers.json").read_text(encoding="utf-8"))
    logs = json.loads(Path("atlas_rapporteur/runtime/audit/provider_run_log.json").read_text(encoding="utf-8"))
    assert any(s["status"] == "SKIPPED_DISABLED" for s in skipped)
    assert isinstance(logs, list) and logs


def test_discover_aucun_resultat_fictif(monkeypatch):
    monkeypatch.delenv("BRAVE_SEARCH_API_KEY", raising=False)
    monkeypatch.delenv("TAVILY_API_KEY", raising=False)
    leads, _ = run("discover", limit=5, with_summary=True)
    assert all("example.com" not in l.source_url for l in leads)


def test_aucun_business_ready_sans_validation_humaine():
    leads = run("discover", limit=5)
    assert all(l.qualification_status != "BUSINESS_READY" for l in leads)
