POLICY = {
    "termux_mvp": "local_single_tenant",
    "early_saas": "shared_db_tenant_id",
    "serious_b2b": "schema_per_tenant",
    "regulated_enterprise": "database_per_tenant|dedicated_stack",
}

def deny_cross_tenant(actor_tenant_id: str, resource_tenant_id: str):
    if actor_tenant_id != resource_tenant_id:
        raise PermissionError("cross-tenant access refused")
