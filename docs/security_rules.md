# Security Rules

Forbidden in repository:
- full Wikidata dumps
- full Sirene datasets
- Gmail exports
- Google tokens
- credentials files
- real invoices/PDF/payroll/client data

Enforcement:
- use only anonymized fixtures in tests
- all sensitive material in `~/atlas_data`
- delivery refused when role not allowed
- delivery refused if indexed hash changed
