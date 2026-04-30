import json
from atlas_rapporteur.src.budget_guard import can_spend_query, register_query_cost, stop_reason_if_blocked, USAGE_PATH
from atlas_rapporteur.src.main import run


def test_budget_stop_avant_requete(monkeypatch):
    monkeypatch.setenv("SEARCH_DAILY_LIMIT", "0")
    assert not can_spend_query()
    assert stop_reason_if_blocked() == "max_queries_per_day_reached"


def test_google_cse_budget_exceeded_mock(monkeypatch):
    monkeypatch.setenv("GOOGLE_CSE_API_KEY", "k")
    monkeypatch.setenv("GOOGLE_CSE_CX", "cx")
    monkeypatch.setenv("SEARCH_DAILY_LIMIT", "1")
    USAGE_PATH.parent.mkdir(parents=True, exist_ok=True)
    USAGE_PATH.write_text("[]", encoding="utf-8")
    register_query_cost("already-spent")
    _, summary = run("google-cse", limit=20, with_summary=True)
    assert summary["stopped_by_budget"] is True
