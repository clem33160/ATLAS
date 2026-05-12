from dataclasses import dataclass
from datetime import datetime, timezone

ISOLATION_MODES = {
    "local_single_tenant",
    "shared_db_tenant_id",
    "schema_per_tenant",
    "database_per_tenant",
    "dedicated_stack",
}

@dataclass(frozen=True)
class Tenant:
    tenant_id: str
    tenant_name: str
    legal_entity_name: str
    country: str
    region: str
    plan: str
    status: str
    created_at: str
    data_region: str
    isolation_mode: str
    billing_account_id: str
    admin_user_id: str

    @staticmethod
    def create(**kwargs):
        kwargs.setdefault("created_at", datetime.now(timezone.utc).isoformat())
        t = Tenant(**kwargs)
        if t.isolation_mode not in ISOLATION_MODES:
            raise ValueError("unsupported isolation mode")
        return t
