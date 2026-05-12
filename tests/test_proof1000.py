from core.proof.proof1000 import run_proof1000

def test_proof1000_v2(tmp_path):
    assert run_proof1000(tmp_path).CRITICAL_FAIL==0
