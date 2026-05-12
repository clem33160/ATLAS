from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import uuid4


def _id() -> str:
    return str(uuid4())


@dataclass
class Tenant:
    name: str
    id: str = field(default_factory=_id)


@dataclass
class User:
    tenant_id: str
    email: str
    role: str
    id: str = field(default_factory=_id)


@dataclass
class Role:
    tenant_id: str
    name: str
    id: str = field(default_factory=_id)


@dataclass
class Client:
    tenant_id: str
    name: str
    id: str = field(default_factory=_id)


@dataclass
class Document:
    tenant_id: str
    title: str
    body: str
    id: str = field(default_factory=_id)


@dataclass
class DocumentProof:
    tenant_id: str
    doc_id: str
    sha256: str
    provenance: str
    delivery_receipt: Optional[str] = None
    id: str = field(default_factory=_id)


@dataclass
class AuditEvent:
    tenant_id: str
    actor: str
    action: str
    created_at: datetime = field(default_factory=datetime.utcnow)
    id: str = field(default_factory=_id)


@dataclass
class ConnectorAccount:
    tenant_id: str
    provider: str
    external_id: str
    id: str = field(default_factory=_id)


@dataclass
class Job:
    tenant_id: str
    type: str
    status: str
    id: str = field(default_factory=_id)


@dataclass
class Quote:
    tenant_id: str
    client_id: str
    amount_cents: int
    id: str = field(default_factory=_id)


@dataclass
class Invoice:
    tenant_id: str
    client_id: str
    amount_cents: int
    id: str = field(default_factory=_id)


@dataclass
class Payment:
    tenant_id: str
    invoice_id: str
    amount_cents: int
    id: str = field(default_factory=_id)


@dataclass
class Subscription:
    tenant_id: str
    plan: str
    status: str
    id: str = field(default_factory=_id)


@dataclass
class UsageEvent:
    tenant_id: str
    metric: str
    value: int
    id: str = field(default_factory=_id)
