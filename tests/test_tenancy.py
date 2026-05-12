from core.tenancy.tenant import Tenant
from core.tenancy.registry import TenantRegistry
from core.tenancy.isolation import deny_cross_tenant

def test_tenant_model_and_registry():
    t=Tenant.create(tenant_id='t1',tenant_name='T1',legal_entity_name='L1',country='FR',region='EU',plan='pilot_local',status='active',data_region='eu',isolation_mode='local_single_tenant',billing_account_id='b1',admin_user_id='u1')
    r=TenantRegistry(); r.create(t)
    assert r.get('t1').tenant_name=='T1'

def test_isolation_refusal():
    try: deny_cross_tenant('A','B'); assert False
    except PermissionError: assert True
