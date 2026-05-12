from core.tenancy.tenant import Tenant
from core.tenancy.registry import TenantRegistry

def setup_tenant(registry:TenantRegistry, **kwargs):
    t=Tenant.create(**kwargs); registry.create(t); return t
