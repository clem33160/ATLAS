from core.tenancy.tenant import Tenant

class TenantRegistry:
    def __init__(self): self._tenants = {}
    def create(self, tenant: Tenant):
        if tenant.tenant_id in self._tenants: raise ValueError("tenant exists")
        self._tenants[tenant.tenant_id] = tenant
    def get(self, tenant_id: str) -> Tenant:
        return self._tenants[tenant_id]
    def all(self): return list(self._tenants.values())
