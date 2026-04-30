from atlas_memory.src.integration import ingest_rapporteur_run

def test_ingest_rapporteur_no_crash():
    r=ingest_rapporteur_run()
    assert set(r.keys())=={'summary','rejected','leads'}
