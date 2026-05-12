# 10 000 clients local simulation proof

Cette preuve locale exécute une simulation déterministe sans PDF réels lourds.

- 10 000 tenants
- 50 000 users (5 par tenant)
- 500 000 documents simulés (metadata en mémoire)
- isolation tenant stricte
- search tenant-scoped (facture client, devis, relance, document inconnu)
- delivery avec receipt (tenant_id, doc_id, sha256, timestamp, role, decision)
- RBAC par rôles
- audit events + vérification de chaîne audit échantillonnée
- backup manifest + restore simulation
- usage/quotas + mesures de performance

## Commande CLI

```bash
./scripts/atlas proof10000-clients
```

Sortie visée :
- `CRITICAL_FAIL: 0`
- `Decision: PROOF10000_CLIENTS_PASS`
- `Public SaaS-ready: NO` (via readiness)
- `Production-ready: NO`
