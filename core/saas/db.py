from __future__ import annotations

from typing import Any

try:
    from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
    from sqlalchemy.orm import declarative_base
    from sqlalchemy.sql import func
except Exception:  # pragma: no cover
    declarative_base = None
    Column = DateTime = ForeignKey = Integer = String = Text = func = Any


Base = declarative_base() if declarative_base else object


if declarative_base:
    class TenantORM(Base):
        __tablename__ = "tenants"
        id = Column(String, primary_key=True)
        name = Column(String, nullable=False)

    class UserORM(Base):
        __tablename__ = "users"
        id = Column(String, primary_key=True)
        tenant_id = Column(String, ForeignKey("tenants.id"), nullable=False, index=True)
        email = Column(String, nullable=False)
        role = Column(String, nullable=False)

    class RoleORM(Base):
        __tablename__ = "roles"
        id = Column(String, primary_key=True)
        tenant_id = Column(String, ForeignKey("tenants.id"), nullable=False, index=True)
        name = Column(String, nullable=False)

    class ClientORM(Base):
        __tablename__ = "clients"
        id = Column(String, primary_key=True)
        tenant_id = Column(String, ForeignKey("tenants.id"), nullable=False, index=True)
        name = Column(String, nullable=False)

    class DocumentORM(Base):
        __tablename__ = "documents"
        id = Column(String, primary_key=True)
        tenant_id = Column(String, ForeignKey("tenants.id"), nullable=False, index=True)
        title = Column(String, nullable=False)
        body = Column(Text, nullable=False)

    class DocumentProofORM(Base):
        __tablename__ = "document_proofs"
        id = Column(String, primary_key=True)
        tenant_id = Column(String, ForeignKey("tenants.id"), nullable=False, index=True)
        doc_id = Column(String, ForeignKey("documents.id"), nullable=False, index=True)
        sha256 = Column(String, nullable=False)
        provenance = Column(Text, nullable=False)
        delivery_receipt = Column(Text)

    class AuditEventORM(Base):
        __tablename__ = "audit_events"
        id = Column(String, primary_key=True)
        tenant_id = Column(String, ForeignKey("tenants.id"), nullable=False, index=True)
        actor = Column(String, nullable=False)
        action = Column(String, nullable=False)
        created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    class ConnectorAccountORM(Base):
        __tablename__ = "connector_accounts"
        id = Column(String, primary_key=True)
        tenant_id = Column(String, ForeignKey("tenants.id"), nullable=False, index=True)
        provider = Column(String, nullable=False)
        external_id = Column(String, nullable=False)

    class JobORM(Base):
        __tablename__ = "jobs"
        id = Column(String, primary_key=True)
        tenant_id = Column(String, ForeignKey("tenants.id"), nullable=False, index=True)
        type = Column(String, nullable=False)
        status = Column(String, nullable=False)

    class QuoteORM(Base):
        __tablename__ = "quotes"
        id = Column(String, primary_key=True)
        tenant_id = Column(String, ForeignKey("tenants.id"), nullable=False, index=True)
        client_id = Column(String, ForeignKey("clients.id"), nullable=False)
        amount_cents = Column(Integer, nullable=False)

    class InvoiceORM(Base):
        __tablename__ = "invoices"
        id = Column(String, primary_key=True)
        tenant_id = Column(String, ForeignKey("tenants.id"), nullable=False, index=True)
        client_id = Column(String, ForeignKey("clients.id"), nullable=False)
        amount_cents = Column(Integer, nullable=False)

    class PaymentORM(Base):
        __tablename__ = "payments"
        id = Column(String, primary_key=True)
        tenant_id = Column(String, ForeignKey("tenants.id"), nullable=False, index=True)
        invoice_id = Column(String, ForeignKey("invoices.id"), nullable=False)
        amount_cents = Column(Integer, nullable=False)

    class SubscriptionORM(Base):
        __tablename__ = "subscriptions"
        id = Column(String, primary_key=True)
        tenant_id = Column(String, ForeignKey("tenants.id"), nullable=False, index=True)
        plan = Column(String, nullable=False)
        status = Column(String, nullable=False)

    class UsageEventORM(Base):
        __tablename__ = "usage_events"
        id = Column(String, primary_key=True)
        tenant_id = Column(String, ForeignKey("tenants.id"), nullable=False, index=True)
        metric = Column(String, nullable=False)
        value = Column(Integer, nullable=False)
