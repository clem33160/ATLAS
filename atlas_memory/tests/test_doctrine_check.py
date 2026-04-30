from atlas_memory.src.doctrine_check import run_doctrine_check

def test_doctrine_has_20_and_7():
    r=run_doctrine_check()
    assert r['layers_count']==20
    assert r['questions_count']==7
