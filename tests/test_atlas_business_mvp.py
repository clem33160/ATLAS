from pathlib import Path

from core.config.settings import load_paths
from core.data_sources.registry import build_registry
from core.documents.engine import DocumentEngine
from core.proof.proof1000 import run_proof1000


def test_config_paths_load(tmp_path: Path):
    cfg = tmp_path / "atlas.config.yaml"
    cfg.write_text(
        """
paths:
  wikidata_dump: ~/atlas_data/wikidata/latest-truthy.nt
  sirene_data: ~/atlas_data/sirene/sirene_light.csv
  document_root: ~/atlas_data/documents
  indexes_path: ~/atlas_data/indexes
  google_token_path: ~/atlas_data/secrets/google_token.json
  gmail_import_path: ~/atlas_data/imports/gmail
  sandbox_test_path: ~/atlas_data/sandbox/proof1000
""",
        encoding="utf-8",
    )
    paths = load_paths(cfg)
    assert str(paths.document_root).endswith("atlas_data/documents")


def test_source_registry_contract():
    from core.config.miniyaml import load_simple_yaml
    payload = load_simple_yaml("atlas.config.example.yaml")
    registry = build_registry(payload["sources"])
    assert registry and registry[0].source_id == "wikidata_local"


def test_document_engine_refusals(tmp_path: Path):
    engine = DocumentEngine()
    a = tmp_path / "invoice_a.txt"
    b = tmp_path / "invoice_b.txt"
    a.write_text("x", encoding="utf-8")
    b.write_text("y", encoding="utf-8")
    p = engine.index_document(a)
    engine.index_document(b)

    try:
        engine.require_unambiguous_match("invoice")
        assert False
    except ValueError as err:
        assert "choices=" in str(err)

    assert engine.delivery_by_doc_id(p.doc_id, "admin") == a.resolve()


def test_proof1000(tmp_path: Path):
    result = run_proof1000(tmp_path / "proof1000")
    assert result.CRITICAL_FAIL == 0
