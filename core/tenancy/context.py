from contextvars import ContextVar
_tenant_ctx: ContextVar[str | None] = ContextVar("tenant_id", default=None)

def set_tenant(tenant_id: str):
    return _tenant_ctx.set(tenant_id)

def get_tenant() -> str | None:
    return _tenant_ctx.get()
