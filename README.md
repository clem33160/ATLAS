# ATLAS — Rapporteur d’Affaires (V0.3)

Cette V0.3 fournit une démo locale **sans internet** pour:
- ingérer des signaux publics de démonstration,
- scorer des leads,
- matcher des artisans,
- générer un rapport Markdown enrichi,
- générer un export JSON + CSV.

## Structure

- `atlas/config/cities.yaml` : config métiers/villes (priorités)
- `atlas/data/sources/demo_public_signals.json` : sources publiques démo
- `atlas/data/artisans/demo_artisans.json` : artisans démo
- `atlas/main.py` : pipeline complet V0.3
- `atlas/scripts/run.sh` : lancement de la démo
- `atlas/scripts/test.sh` : exécution des tests
- `atlas/examples/` : exemples versionnés (statiques)
- `atlas/runtime/` : sorties générées localement (runtime, ignorées par Git)

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
- un rapport Markdown est disponible dans `atlas/runtime/reports/lead_report.md`
- un export JSON est disponible dans `atlas/runtime/export/leads_ranked.json`
- un export CSV est disponible dans `atlas/runtime/export/leads_ranked.csv`
- un résumé est disponible dans `atlas/runtime/outputs/run_summary.json`

## Mise à jour du dépôt depuis Termux

Pour éviter les conflits liés à des fichiers locaux générés, utilisez:

```bash
git pull --rebase --autostash
```

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

3. Mettre à jour le dépôt:

```bash
git pull --rebase --autostash
```

4. Lancer la démo locale (sans internet):

```bash
./atlas/scripts/run.sh
```

5. Lancer les tests:

```bash
./atlas/scripts/test.sh
```

6. Vérifier les sorties:
- `atlas/runtime/reports/lead_report.md`
- `atlas/runtime/export/leads_ranked.json`
- `atlas/runtime/export/leads_ranked.csv`
- `atlas/runtime/outputs/run_summary.json` (résumé d’exécution)
