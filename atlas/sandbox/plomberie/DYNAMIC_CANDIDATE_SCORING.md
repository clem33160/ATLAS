# DYNAMIC CANDIDATE SCORING

Scores 0-100 par dimension:
CRM completeness, call intake quality, safety handling, compliance, invoice workflow, chantier workflow, client follow-up, field memory, business value, test coverage, maintainability, explainability, no-regression confidence.

Règles:
- score critique minimum: sécurité>=85, conformité>=85, no-regression>=80
- score global: moyenne pondérée
- seuil acceptation: global>=90 et aucun critique en baisse
- seuil refus: toute baisse critique ou global<75
- plateau: variation <1 point sur 3 cycles
- next mission recommendation: dimension la plus faible sans régression.
