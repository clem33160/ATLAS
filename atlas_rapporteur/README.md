# Atlas Rapporteur d’Affaires — Clean V1

Base canonique pour détecter des opportunités **publiques** de travaux dans la francophonie, les qualifier, scorer, matcher des artisans vérifiables, et produire des fiches pour un closer humain.

## Principes de conformité
- Sources publiques uniquement, sans login/captcha bypass.
- Pas de scraping agressif, spam, ni contact automatique.
- Aucune invention de lead ou d’artisan.
- Si une donnée manque: `INCONNU`.
- Validation humaine obligatoire avant état business critique.

## Installation rapide
```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt  # optionnel, le projet tourne sans dépendances externes
```

## Variables d’environnement
- `GOOGLE_CSE_API_KEY`
- `GOOGLE_CSE_CX`
- `OPENAI_API_KEY`
- `ATLAS_ANALYSIS_MODEL` (défaut: `gpt-5.4`)
- `ATLAS_DRY_RUN` (défaut: `1`)

## Commandes
```bash
bash atlas_rapporteur/scripts/init_db.sh
bash atlas_rapporteur/scripts/test.sh
bash atlas_rapporteur/scripts/run.sh --dry-run
bash atlas_rapporteur/scripts/run.sh --manual
bash atlas_rapporteur/scripts/run.sh --google-cse --limit 20
bash atlas_rapporteur/scripts/audit.sh
```

## Modes d’exécution
- `--dry-run`: fixtures offline.
- `--manual`: lit `inbox/manual_urls.csv`.
- `--google-cse`: actif seulement si clés présentes, sinon fallback dry-run.

## Sorties
- `runtime/exports/leads_ranked.json`
- `runtime/exports/leads_ranked.csv`
- `runtime/reports/daily_report.md`
- `runtime/closer/closer_call_sheet.md`
- `runtime/audit/audit_report.md`

## Règle anti-faux lead
Seuls `CLIENT_REQUEST` et `PUBLIC_MARKET` sont conservés comme opportunités potentielles.
