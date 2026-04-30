from atlas_rapporteur.src.models import Lead
from atlas_rapporteur.src.scoring import score_lead

def test_scoring_range():
    l=Lead(title='x',url='u',snippet='s',city='Lyon',country='France',trade='plomberie',intent_type='CLIENT_REQUEST',urgency='URGENT',source_domain='a',contact_public='OUI')
    l=score_lead(l)
    assert 0 <= l.score <= 100
