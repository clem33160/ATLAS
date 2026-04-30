from pathlib import Path
from atlas_rapporteur.src.main import run
from atlas_rapporteur.src.query_optimizer import build_query_candidates


def test_query_builder_city_trade_intent():
    qs = build_query_candidates(5, country="FR", city="Lyon", trade="plomberie")
    assert qs and "lyon" in qs[0]["query"].lower() and "plomberie" in qs[0]["query"].lower()


def test_query_performance_written():
    run("dry-run", limit=5)
    assert Path("atlas_rapporteur/runtime/query_lab/query_performance.json").exists()


def test_next_queries_generated():
    run("dry-run", limit=5)
    assert Path("atlas_rapporteur/runtime/query_lab/next_queries.json").exists()
