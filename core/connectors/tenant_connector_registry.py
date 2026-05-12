class TenantConnectorRegistry:
    def __init__(self): self.data={}
    def link(self, tenant_id:str, connector:str, token_ref:str):
        self.data.setdefault(tenant_id,{})[connector]=token_ref
    def revoke_all(self, tenant_id:str):
        self.data[tenant_id]={}
