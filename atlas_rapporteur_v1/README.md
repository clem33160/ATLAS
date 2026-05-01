# Atlas Rapporteur V1

Pipeline: source -> raw -> normalized -> candidates -> scored -> report.

Architecture:
- `connectors/`: collecteurs légaux publics.
- `core/`: normalisation, déduplication, classification, scoring, conformité, commission, reporting.
- `scripts/atlas_50_leads.sh`: commande principale robuste qui retourne 0 même sans lead.
- `runtime/`: artefacts d'exécution.

Limitation actuelle: seul BOAMP est implémenté réellement; PLACE/TED/SEAO/CanadaBuys sont des stubs `NOT_IMPLEMENTED`.
