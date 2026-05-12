from pathlib import Path
import hashlib
from core.documents.tenant_index import TenantDocumentIndex
from core.documents.tenant_search import search_by_doc_id
from core.documents.tenant_delivery import deliver_tenant_doc

def test_tenant_document_flow(tmp_path:Path):
    f=tmp_path/'x.txt'; f.write_text('x')
    idx=TenantDocumentIndex(); d=idx.index('A',{'doc_id':'1','path':str(f),'sha256':hashlib.sha256(b'x').hexdigest()})
    assert search_by_doc_id(idx,'A','1')['status']=='unique'
    assert search_by_doc_id(idx,'B','1')['status']=='not_found'
    assert deliver_tenant_doc(d,'A',tmp_path/'out')['status']=='ok'
