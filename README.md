# Atlas Rapporteur d’Affaires (V0.7)

V0.7 transforme Atlas en moteur de collecte **semi-automatique légale** à partir d’URLs publiques fournies manuellement.

## Statuts réalité
- `DEMO`
- `MANUAL`
- `COLLECTED_FROM_URL`
- `PARTIALLY_VERIFIED`
- `HUMAN_CONFIRMED`
- `ARCHIVED`

## Entrées utilisateur
- URLs: `atlas/inbox/source_urls.txt` (1 URL publique par ligne)
- Leads manuels: `atlas/inbox/leads_manual_example.json|csv`
- Artisans manuels: `atlas/inbox/artisans_manual.csv|json` (ou exemples)
- Retours d’appel: `atlas/inbox/call_updates.csv`

## Règles légales et interdictions
Aucun spam, aucun contact automatique, aucun bypass captcha/login/ToS, aucun scraping agressif.
Toujours: **Validation humaine des conditions du site requise.**

## Exports
- Rapport: `atlas/runtime/reports/lead_report.md`
- Closer: `atlas/runtime/closer/daily_call_sheet.md`
- Ranking: `atlas/runtime/export/leads_ranked.json|csv`
- Evidence: `atlas/runtime/evidence/source_fetch_log.json`

## Workflow Codex Web + GitHub + Termux
```bash
cd "$HOME/atlas_workspace/ATLAS"
git pull --rebase --autostash
chmod +x ./atlas/scripts/run.sh ./atlas/scripts/test.sh
./atlas/scripts/test.sh
./atlas/scripts/run.sh
sed -n '1,360p' atlas/runtime/reports/lead_report.md
sed -n '1,260p' atlas/runtime/closer/daily_call_sheet.md
```

## Modes
- Run: `./atlas/scripts/run.sh`
- CRM summary: `./atlas/scripts/run.sh crm-summary`
- Verbose: `./atlas/scripts/run.sh verbose`
