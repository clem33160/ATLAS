# Atlas Rapporteur d’Affaires V0.9 - Business réel et anti-hallucination

Atlas V0.9 vise un socle business réel et vérifiable.

- Objectif futur: **50 leads/jour**.
- V0.9 **ne promet pas** 50 vrais leads/jour.
- Les vrais leads exigent des URLs publiques précises + validation humaine.
- Aucun lead/artisan/téléphone/site inventé comme réel.

## Ajouter des URLs

Remplir `atlas/inbox/source_urls.txt`:

- `url`
- ou `source_id|url|note|country|city_hint|trade_hint`

## Ajouter des artisans vérifiables

- importer des artisans manuels avec `source_url`
- privilégier sources officielles (RGE/SIRENE/annuaires)

## Ajouter les retours d’appels

- alimenter le CRM runtime via process humain (aucune auto-invention)

## Lire le score business

- `atlas/runtime/business/business_readiness.json`
- `atlas/runtime/business/business_readiness.md`

Le score affiche:
- score actuel
- score maximal avec données disponibles
- blocages vers 10/10
- actions concrètes pour progresser

## Commandes

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
