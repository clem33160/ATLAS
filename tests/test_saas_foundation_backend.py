from core.saas.backend import TenantScopedStore, create_app


def test_tenant_isolation_and_proof_refusal():
    store = TenantScopedStore()
    a = store.create_tenant("A")
    b = store.create_tenant("B")
    doc = store.create_document(a.id, "invoice", "body-a", "upload")

    assert len(store.list_documents(a.id)) == 1
    assert len(store.list_documents(b.id)) == 0

    try:
        store.verify_document_integrity(b.id, doc.id, "body-a")
        assert False
    except PermissionError:
        assert True

    try:
        store.verify_document_integrity(a.id, doc.id, "changed")
        assert False
    except ValueError as exc:
        assert "hash changed refusal" in str(exc)


def test_app_endpoints_and_readiness_contract():
    app = create_app(TenantScopedStore())
    paths = {route[1] for route in app.routes.keys()} if hasattr(app, "routes") and isinstance(app.routes, dict) else set()
    for p in ["/health", "/tenants", "/users", "/documents", "/search", "/delivery", "/audit", "/readiness"]:
        assert p in paths

    payload = app.routes[("GET", "/readiness")]()
    assert payload["public_saas_ready"] is False
    assert payload["pilot_ready"] is True
