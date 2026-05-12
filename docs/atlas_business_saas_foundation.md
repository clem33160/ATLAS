# Atlas Business SaaS Foundation

## SaaS architecture
- API layer: FastAPI-compatible app factory (`core/saas/backend.py`).
- Data layer: PostgreSQL-ready SQLAlchemy schema definitions (`core/saas/db.py`) plus in-memory store for current pilot runtime.
- Tenant boundary: all protected flows are `tenant_id` scoped with explicit cross-tenant refusal.
- Proof layer: SHA-256 + provenance + delivery receipt placeholder in `DocumentProof`.
- Connectors: mockable interfaces for Gmail, Drive, Calendar, Sheets.
- Jobs: worker skeleton for document import, OCR, classification, indexing, connector sync.
- Storage: local dev storage under `~/atlas_data/storage`; S3-compatible contract ready for production adapter.

## Local deployment
1. Install app dependencies (`fastapi`, `uvicorn`, `sqlalchemy`) when runtime API serving is needed.
2. Start API by importing `create_app` from `core.saas`.
3. Persist local assets in `~/atlas_data` (not `/tmp`).

## Production roadmap
- Add real PostgreSQL engine/session wiring and migrations.
- Add authN/authZ middleware + service identities.
- Replace in-memory jobs with durable queue/worker runtime.
- Replace mock connectors with secure OAuth token vault integration.
- Add object store implementation for S3-compatible backends.

## Current blockers
- No production-grade authentication.
- No durable background job queue.
- No DB migration toolchain integrated.
- No production connector token lifecycle.

## Pilot-ready scope
- Tenant-scoped domain model foundation.
- Role vocabulary and access refusal primitives.
- Proof hashing and tamper refusal checks.
- API contract skeleton and test coverage for isolation/readiness behavior.

## Not SaaS-ready yet
- Not public multi-tenant internet deployment ready.
- Not large-scale concurrency or 5M-user readiness.
- Not compliance-certified nor hardened for hostile production traffic.
