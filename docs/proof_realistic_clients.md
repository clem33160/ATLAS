# ATLAS PROOF REALISTIC CLIENTS

Simulation synthétique de clients artisans avec documents fictifs (.txt/.pdf texte), requêtes humaines ambiguës, contrôle d'accès par rôle, refus sur changement SHA et gestion de scans dégradés.

- Données: 10 tenants métiers, 100 clients finaux fictifs, 500+ documents synthétiques.
- Sécurité: refus apprenti sur RIB/bulletins, refus client externe hors périmètre, comptable limité finance, patron autorisé tenant.
- Ambiguïtés: requêtes `facture Dupont`, `scan_001`, `fuite` => choix numérotés ou validation humaine.
- Intégrité: SHA recalculé; refus de livraison si contenu modifié après indexation.
- Honest claims: `Production-ready: NO`, `Public SaaS-ready: NO`.
