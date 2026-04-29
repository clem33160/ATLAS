# Atlas Rapporteur d’Affaires V0.10 — Nettoyage canonique et qualité code

La V0.10 stabilise l’existant : architecture claire, responsabilités séparées, pipeline lisible, tests renforcés.

- V0.10 **n’ajoute pas de gros nouveau scraping**.
- Atlas **ne produit pas encore automatiquement 50 vrais leads/jour**.
- **50 leads/jour** reste un objectif futur.
- Un business 10/10 exige : URLs réelles, artisans vérifiables, retours d’appels, validation humaine.
- Les données DEMO ne doivent jamais être appelées ni vendues comme réelles.

## Règles anti-faux réel

- Aucun lead DEMO en `BUSINESS_READY`.
- Aucun domaine `example.org`, `example.local`, `example.com` en preuve réelle.
- Aucun `HUMAN_CONFIRMED` sans action CRM humaine.

## Ajouter des URLs publiques

Éditer `atlas/inbox/source_urls.txt` (format `source_id|url|note` ou `url`).

## Ajouter des artisans vérifiables

Utiliser des fiches artisan avec URL vérifiable (source officielle/annuaire pro) dans `atlas/inbox/`.

## Vérifier Business Readiness

- `atlas/runtime/business/business_readiness.json`
- `atlas/runtime/business/business_readiness.md`

Le rapport indique score actuel, plafond actuel, blocages et actions exactes.

## Commandes Termux

```bash
cd "$HOME/atlas_workspace/ATLAS"
git pull --rebase --autostash
chmod +x ./atlas/scripts/*.sh
./atlas/scripts/source_audit.sh
./atlas/scripts/test.sh
./atlas/scripts/run.sh
./atlas/scripts/run.sh business
./atlas/scripts/run.sh closer
./atlas/scripts/business_check.sh
sed -n '1,420p' atlas/runtime/reports/lead_report.md
sed -n '1,360p' atlas/runtime/closer/daily_call_sheet.md
sed -n '1,260p' atlas/runtime/business/business_readiness.md
```
