from pathlib import Path
from atlas_rapporteur.src.feedback_loop import run_feedback_loop

def test_feedback_summary_written():
    run_feedback_loop()
    assert Path("atlas_rapporteur/runtime/query_lab/feedback_summary.json").exists()
