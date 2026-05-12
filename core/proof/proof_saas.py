from pathlib import Path
from core.tenancy.registry import TenantRegistry
from core.tenancy.tenant import Tenant
from core.documents.tenant_index import TenantDocumentIndex
from core.documents.tenant_search import search_by_doc_id
from core.documents.tenant_delivery import deliver_tenant_doc
from core.proof.tenant_audit import TenantAuditChain
from core.billing.usage import UsageLedger
from core.backup.snapshot import build_snapshot_manifest
from core.privacy.export_request import new_export_request

def run_proof_saas(tmp:Path):
    reg=TenantRegistry(); idx=TenantDocumentIndex(); audit=TenantAuditChain(); usage=UsageLedger()
    ta=Tenant.create(tenant_id='A',tenant_name='A',legal_entity_name='A LLC',country='FR',region='EU',plan='artisan_basic',status='active',data_region='eu-west',isolation_mode='shared_db_tenant_id',billing_account_id='ba',admin_user_id='ua')
    tb=Tenant.create(tenant_id='B',tenant_name='B',legal_entity_name='B LLC',country='FR',region='EU',plan='artisan_basic',status='active',data_region='eu-west',isolation_mode='shared_db_tenant_id',billing_account_id='bb',admin_user_id='ub')
    reg.create(ta); reg.create(tb)
    fa=tmp/'a.txt'; fb=tmp/'b.txt'; fa.write_text('A'); fb.write_text('B')
    import hashlib
    da=idx.index('A',{'doc_id':'1','path':str(fa),'sha256':hashlib.sha256(b'A').hexdigest()})
    db=idx.index('B',{'doc_id':'1','path':str(fb),'sha256':hashlib.sha256(b'B').hexdigest()})
    assert search_by_doc_id(idx,'A','1')['doc']['tenant_id']=='A'
    blocked=False
    try: deliver_tenant_doc(db,'A',tmp/'out')
    except PermissionError: blocked=True
    audit.append('A','document_imported',{'doc':'1'}); audit.append('B','document_imported',{'doc':'1'})
    usage.add('A','documents_imported',1)
    snap=build_snapshot_manifest('A',['1'])
    exp=new_export_request('A','ua')
    return {"blocked_cross_tenant_delivery":blocked,"audit_A":audit.verify_tenant('A'),"audit_B":audit.verify_tenant('B'),"usage_A":usage.usage['A']['documents_imported'],"snapshot":snap,"privacy_export":exp,"public_saas_ready":False}
