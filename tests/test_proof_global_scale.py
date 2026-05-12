from pathlib import Path
from core.proof.proof_global_scale import run_proof_global_scale


def test_bounded_global_proof_passes():
    assert run_proof_global_scale(Path('~/atlas_data/sandbox/global_scale').expanduser()).CRITICAL_FAIL == 0
