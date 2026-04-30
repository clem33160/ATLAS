from atlas_rapporteur.src.models import Lead
from atlas_rapporteur.src.compliance import is_potential_lead

def test_anti_blog():
    l=Lead(title='blog',url='u',snippet='s',raw_text_excerpt='article',city='INCONNU',trade='INCONNU',intent_type='BLOG_ARTICLE')
    assert not is_potential_lead(l)

def test_true_client_lead():
    l=Lead(title='cherche plombier',url='u',snippet='s',raw_text_excerpt='x'*80,city='Lyon',trade='plomberie',intent_type='CLIENT_REQUEST')
    assert is_potential_lead(l)
