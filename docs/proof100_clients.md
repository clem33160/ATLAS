# ATLAS proof100-clients

## What is simulated
- 100 isolated tenants with deterministic metadata.
- 500 users (5 roles per tenant).
- 5000 documents (fixed distribution: invoices, quotes, contracts, tax/payment, follow-up).
- Tenant-aware search, delivery, RBAC checks, audit events, backup manifests, and usage counters.

## What is proven
- Local deterministic simulation can generate and validate 100 tenants end-to-end.
- Cross-tenant search/delivery/audit attempts are refused.
- Delivery is exact by `doc_id` and produces receipt metadata.
- Audit chains verify per tenant.
- Backup manifest shape is valid and restore simulation returns `ok`.
- Report ends with `CRITICAL_FAIL=0` when all checks pass.

## What is **not** proven
- Not a production SaaS readiness claim.
- Not a proof of 1000 paying clients.
- Not a proof of internet-scale concurrency, billing integrations, legal compliance operations, or 5M users.

## Termux runbook
Use sandbox path under home, not `/tmp`:

```bash
mkdir -p ~/atlas_data/sandbox/proof100_clients
python -m pytest -q
./scripts/atlas proof100-clients
```

Expected final decision line:

```text
Decision: PROOF100_CLIENTS_PASS
```

## Remaining work before 100 real paying clients
- Production auth/SSO and hardened tenant session boundaries.
- Real backup/restore drills on persistent encrypted storage.
- Billing lifecycle (plans, invoicing, failures, dunning) in production conditions.
- Operational observability/SLOs, incident response, and compliance evidence.
