def can_access_tenant(role:str, actor_tenant_id:str, resource_tenant_id:str, category:str, linked_client:str|None=None, actor_client:str|None=None, auditor_tenants:set[str]|None=None):
    if role=="platform_admin": return True
    if actor_tenant_id != resource_tenant_id: return False
    if role=="external_client": return category=="client_doc" and linked_client==actor_client and linked_client is not None
    if role=="auditor": return category=="proof" and (auditor_tenants is None or actor_tenant_id in auditor_tenants)
    return role in {"owner","secretary","apprentice"}
