# ATLAS — Rapporteur d’Affaires (V0 minimale)

Cette V0 fournit une démo locale **sans internet** pour:
- ingérer des signaux publics de démonstration,
- scorer des leads,
- matcher des artisans,
- générer un rapport Markdown,
- générer un export JSON.

## Structure

- `atlas/config/cities.yaml` : config métiers/villes (priorités)
- `atlas/data/sources/demo_public_signals.json` : sources publiques démo
- `atlas/data/artisans/demo_artisans.json` : artisans démo
- `atlas/main.py` : pipeline complet V0
- `atlas/scripts/run.sh` : lancement de la démo
- `atlas/scripts/test.sh` : exécution des tests
- `atlas/reports/lead_report.md` : rapport généré
- `atlas/export/leads_ranked.json` : export JSON généré
- `atlas/outputs/run_summary.json` : résumé d’exécution

## Exécution

Depuis la racine du dépôt:

```bash
./atlas/scripts/run.sh
```

## Tests

Depuis la racine du dépôt:

```bash
./atlas/scripts/test.sh
```

## Résultat attendu

Après exécution:
- un rapport Markdown est disponible dans `atlas/reports/lead_report.md`
- un export JSON est disponible dans `atlas/export/leads_ranked.json`
- un résumé est disponible dans `atlas/outputs/run_summary.json`
