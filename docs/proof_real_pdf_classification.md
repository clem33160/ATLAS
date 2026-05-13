# ATLAS PROOF REAL PDF CLASSIFICATION

Ce proof génère **100 PDFs synthétiques fictifs** dans `~/atlas_data/sandbox/proof_real_pdf_classification/documents`.

- Données strictement fictives (clients, SIRET, TVA, RIB, salaires, emails).
- Extraction texte avec priorité `pdftotext`, fallback pseudo-PDF, puis fallback sidecar `.txt`.
- Classification métier (facture client, devis, bon intervention, facture fournisseur, contrat entretien, relance impayée, RIB, bulletin salaire, URSSAF, TVA, à vérifier).
- Index avec `sha256`, métadonnées métier, hash du texte extrait et score de confiance.
- Recherche humaine avec statuts `unique`, `ambiguous`, `denied`, `not_found`, `needs_human_validation`.
- Contrôle d'accès par rôle (patron, secrétaire, comptable, apprenti, client externe).
- Refus explicite de livraison si SHA changé (`REFUS_SHA_MODIFIE`).
- Claim de sécurité: **Production-ready: NO**, **Public SaaS-ready: NO**.

Commande CLI:

```bash
./scripts/atlas proof-real-pdf-classification
```
