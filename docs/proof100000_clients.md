# ATLAS PROOF100000 CLIENTS

Cette preuve est une **100 000 clients local simulation proof**.

## Objectif
Valider localement et de façon déterministe la capacité de modéliser :
- 100 000 tenants
- 500 000 users (5 par tenant)
- 5 000 000 documents simulés (50 métadonnées par tenant)

## Méthode d'optimisation
- Aucun PDF réel.
- Aucun lot massif de fichiers JSON individuels.
- Génération déterministe de métadonnées à la demande.
- Compteurs agrégés globaux.
- Échantillonnage représentatif pour search, delivery, RBAC, audit chain et backup.

## Distribution documentaire par tenant
- 15 facture_client
- 8 facture_fournisseur
- 6 devis
- 5 contrat_client
- 4 intervention
- 3 paiement
- 3 relance_impaye
- 2 urssaf
- 2 tva_impot
- 2 a_verifier

## Vérifications
- Isolation cross-tenant : 10 000 refus.
- Search : 10 000 tenants échantillonnés × 4 requêtes.
- Delivery : 10 000 livraisons avec receipt (tenant_id, doc_id, sha256, timestamp, role, decision).
- RBAC : 10 000 cas (apprentice refuse facture_client, external_client refuse non-lié, accountant accepte finance/tax/paiement, owner accepte tout).
- Audit : compteurs globaux + chaîne vérifiée sur 1 000 tenants.
- Backup manifest : shape logique + restore vérifié sur 1 000 tenants.
- Usage/quotas : compteurs consolidés et quota status.

## Commande CLI
```bash
./scripts/atlas proof100000-clients
```
