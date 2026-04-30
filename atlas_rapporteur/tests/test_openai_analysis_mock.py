from atlas_rapporteur.src.models import Lead
from atlas_rapporteur.src.analyzer_openai import analyze_openai_stub

def test_openai_mock_schema():
    l=Lead(title='t',url='u',snippet='s')
    out=analyze_openai_stub(l)
    assert 'is_real_opportunity' in out and 'confidence' in out
