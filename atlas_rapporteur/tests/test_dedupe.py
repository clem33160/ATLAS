from atlas_rapporteur.src.models import Lead
from atlas_rapporteur.src.dedupe import dedupe_leads

def test_dedupe():
    a=Lead(title='A',url='u',snippet='s')
    b=Lead(title='A',url='u',snippet='s')
    assert len(dedupe_leads([a,b]))==1
