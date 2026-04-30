from pathlib import Path
from atlas_rapporteur.src.main import run

def test_dashboard_written():
    run("dry-run", limit=5)
    assert Path("atlas_rapporteur/runtime/dashboard/business_dashboard.md").exists()

def test_exports_written():
    run("dry-run", limit=5)
    assert Path("atlas_rapporteur/runtime/closer/closer_call_sheet.md").exists()
