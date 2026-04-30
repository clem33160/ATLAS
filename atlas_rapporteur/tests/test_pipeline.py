from atlas_rapporteur.src.main import run

def test_dry_run_pipeline():
    leads=run('dry-run',limit=10)
    assert isinstance(leads,list)
