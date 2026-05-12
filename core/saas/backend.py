from __future__ import annotations

import hashlib
from dataclasses import asdict
from typing import Dict, List, Protocol

from core.saas.models import AuditEvent, Document, DocumentProof, Tenant, User

ROLES = {"owner", "secretary", "apprentice", "external_client", "accountant", "auditor"}


class TenantScopedStore:
    def __init__(self) -> None:
        self.tenants: Dict[str, Tenant] = {}
        self.users: Dict[str, User] = {}
        self.documents: Dict[str, Document] = {}
        self.proofs: Dict[str, DocumentProof] = {}
        self.audit: List[AuditEvent] = []

    def _require_tenant(self, tenant_id: str) -> None:
        if tenant_id not in self.tenants:
            raise KeyError("unknown tenant")

    def create_tenant(self, name: str) -> Tenant:
        tenant = Tenant(name=name)
        self.tenants[tenant.id] = tenant
        return tenant

    def list_tenants(self) -> List[Tenant]:
        return list(self.tenants.values())

    def create_user(self, tenant_id: str, email: str, role: str) -> User:
        self._require_tenant(tenant_id)
        if role not in ROLES:
            raise PermissionError("unsupported role")
        user = User(tenant_id=tenant_id, email=email, role=role)
        self.users[user.id] = user
        return user

    def create_document(self, tenant_id: str, title: str, body: str, provenance: str) -> Document:
        self._require_tenant(tenant_id)
        doc = Document(tenant_id=tenant_id, title=title, body=body)
        self.documents[doc.id] = doc
        sha = hashlib.sha256(body.encode("utf-8")).hexdigest()
        self.proofs[doc.id] = DocumentProof(tenant_id=tenant_id, doc_id=doc.id, sha256=sha, provenance=provenance)
        self.audit.append(AuditEvent(tenant_id=tenant_id, actor="system", action=f"document_created:{doc.id}"))
        return doc

    def verify_document_integrity(self, tenant_id: str, doc_id: str, body: str) -> bool:
        doc = self.documents[doc_id]
        if doc.tenant_id != tenant_id:
            raise PermissionError("cross-tenant access refused")
        current = hashlib.sha256(body.encode("utf-8")).hexdigest()
        if self.proofs[doc_id].sha256 != current:
            raise ValueError("hash changed refusal")
        return True

    def list_documents(self, tenant_id: str) -> List[Document]:
        self._require_tenant(tenant_id)
        return [d for d in self.documents.values() if d.tenant_id == tenant_id]


class Connector(Protocol):
    def pull(self, tenant_id: str) -> list[dict]: ...


class MockConnector:
    def __init__(self, name: str):
        self.name = name

    def pull(self, tenant_id: str) -> list[dict]:
        return [{"tenant_id": tenant_id, "connector": self.name, "status": "mocked"}]


CONNECTORS = {k: MockConnector(k) for k in ["gmail", "drive", "calendar", "sheets"]}
JOBS = ["document_import", "ocr", "classification", "indexing", "connector_sync"]


class MinimalFastAPI:
    def __init__(self):
        self.routes = {}

    def get(self, path):
        def dec(fn):
            self.routes[("GET", path)] = fn
            return fn

        return dec

    def post(self, path):
        def dec(fn):
            self.routes[("POST", path)] = fn
            return fn

        return dec


def create_app(store: TenantScopedStore | None = None):
    store = store or TenantScopedStore()
    try:
        from fastapi import FastAPI, HTTPException
        app = FastAPI(title="Atlas Business Foundation")
        error = HTTPException
    except Exception:  # pragma: no cover
        app = MinimalFastAPI()
        class error(Exception):
            def __init__(self, status_code: int, detail: str):
                super().__init__(detail)

    @app.get("/health")
    def health():
        return {"status": "ok"}

    @app.get("/readiness")
    def readiness():
        return {"public_saas_ready": False, "pilot_ready": True, "blockers": ["no production auth", "no durable worker queue"]}

    @app.get("/tenants")
    def tenants():
        return [asdict(x) for x in store.list_tenants()]

    @app.post("/users")
    def users(tenant_id: str, email: str, role: str):
        try:
            return asdict(store.create_user(tenant_id, email, role))
        except Exception as exc:
            raise error(status_code=403, detail=str(exc))

    @app.post("/documents")
    def documents(tenant_id: str, title: str, body: str, provenance: str):
        try:
            return asdict(store.create_document(tenant_id, title, body, provenance))
        except Exception as exc:
            raise error(status_code=403, detail=str(exc))

    @app.get("/search")
    def search(tenant_id: str, q: str):
        docs = [asdict(d) for d in store.list_documents(tenant_id) if q.lower() in d.title.lower() or q.lower() in d.body.lower()]
        return {"items": docs}

    @app.get("/delivery")
    def delivery(tenant_id: str, doc_id: str):
        proof = store.proofs.get(doc_id)
        if not proof or proof.tenant_id != tenant_id:
            raise error(status_code=403, detail="cross-tenant access refused")
        return {"doc_id": doc_id, "delivery_receipt": proof.delivery_receipt or "pending"}

    @app.get("/audit")
    def audit(tenant_id: str):
        return [asdict(a) for a in store.audit if a.tenant_id == tenant_id]

    return app
