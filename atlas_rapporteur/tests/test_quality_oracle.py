from pathlib import Path
from atlas_rapporteur.src.main import run

def test_rejected_results_has_reasons():
    run("dry-run", limit=5)
    assert Path("atlas_rapporteur/runtime/audit/rejected_results.json").exists()
