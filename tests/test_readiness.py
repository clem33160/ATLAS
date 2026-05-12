from core.readiness.scoring import readiness_score

def test_readiness_honest():
    r=readiness_score({'Connectors':8})
    assert r['score_10'] < 10
