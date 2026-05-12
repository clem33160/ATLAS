from pathlib import Path
from core.documents.classifier import classify
from core.documents.search import search_docs
from core.documents.delivery import deliver

def test_classifier_priority():
    assert classify('facture_dupont.pdf','TVA incluse') == 'facture_client'

def test_search_and_delivery(tmp_path: Path):
    f=tmp_path/'a.txt'; f.write_text('x')
    import hashlib
    d={'doc_id':'DOC_1','path':str(f),'sha256':hashlib.sha256(b'x').hexdigest(),'provenance':{}}
    assert search_docs([d],'DOC_1')['status']=='unique'
    r=deliver(d,'owner',tmp_path/'out','invoice')
    assert r['doc_id']=='DOC_1'
