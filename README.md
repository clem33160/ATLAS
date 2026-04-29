# ATLAS — Rapporteur d’Affaires (V0.2)

Cette V0 fournit une démo locale **sans internet** pour:
- ingérer des signaux publics de démonstration,
- scorer des leads,
- matcher des artisans,
- générer un rapport Markdown enrichi,
- générer un export JSON + CSV.

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
- un export CSV est disponible dans `atlas/export/leads_ranked.csv`
- un résumé est disponible dans `atlas/outputs/run_summary.json`

## Procédure Termux (Android)

1. Installer les paquets requis:

```bash
pkg update -y && pkg upgrade -y
pkg install -y git python
```

2. Cloner le dépôt et se placer dedans:

```bash
git clone <URL_DU_DEPOT> ATLAS
cd ATLAS
```

3. Lancer la démo locale (sans internet):

```bash
./atlas/scripts/run.sh
```

4. Lancer les tests:

```bash
./atlas/scripts/test.sh
```

5. Vérifier les sorties:
- `atlas/reports/lead_report.md`
- `atlas/export/leads_ranked.json`
- `atlas/export/leads_ranked.csv`
- `atlas/outputs/run_summary.json` (résumé d’exécution)
