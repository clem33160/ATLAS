import io
import json
import urllib.error

from atlas_rapporteur.src.search_google_cse import search_google_cse


class Resp:
    def __init__(self, payload):
        self.payload = payload
    def read(self):
        return json.dumps(self.payload).encode("utf-8")
    def __enter__(self):
        return self
    def __exit__(self, *args):
        return False


def test_google_cse_mock_pagination(monkeypatch):
    monkeypatch.setenv("GOOGLE_CSE_API_KEY", "k")
    monkeypatch.setenv("GOOGLE_CSE_CX", "cx")
    calls = {"n": 0}
    def fake_open(url, timeout=10):
        calls["n"] += 1
        if calls["n"] == 1:
            return Resp({"items": [{"title": "T1", "link": "https://x/1", "snippet": "cherche plomberie Lyon"}], "queries": {"nextPage": [{"startIndex": 11}]}})
        return Resp({"items": [{"title": "T2", "link": "https://x/2", "snippet": "devis plomberie Lyon"}]})
    monkeypatch.setattr("urllib.request.urlopen", fake_open)
    items, used = search_google_cse([{"query": "q", "city": "Lyon", "country": "FR", "trade": "plomberie"}], limit=2)
    assert len(items) == 2 and used == 2


def test_google_cse_mock_quota_exceeded(monkeypatch):
    monkeypatch.setenv("GOOGLE_CSE_API_KEY", "k")
    monkeypatch.setenv("GOOGLE_CSE_CX", "cx")
    def fake_open(url, timeout=10):
        raise urllib.error.HTTPError(url, 429, "quota", {}, io.BytesIO())
    monkeypatch.setattr("urllib.request.urlopen", fake_open)
    try:
        search_google_cse([{"query": "q"}], limit=1)
    except RuntimeError as e:
        assert "quota" in str(e)
    else:
        assert False
