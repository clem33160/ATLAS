# Atlas Rapporteur d’Affaires — V0 Production

Backend Python déployable pour détecter/qualifier des leads publics BTP via API de recherche compatible Google CSE.

## Variables d'environnement
- `SEARCH_PROVIDER` (`google_cse` ou autre provider)
- `GOOGLE_SEARCH_API_KEY`
- `GOOGLE_SEARCH_ENGINE_ID`
- `SEARCH_MONTHLY_BUDGET_EUR` (ex: 150)
- `SEARCH_DAILY_LIMIT` (ex: 80)
- `SEARCH_COST_PER_QUERY_EUR` (ex: 0.005)
- `SEARCH_MAX_AGE_DAYS` (ex: 15)

## Installation
```bash
python -m venv .venv
. .venv/bin/activate
pip install pytest
```

## Commandes
```bash
PYTHONPATH=. python -m atlas_rapporteur.src.main --mode dry-run --limit 50
PYTHONPATH=. python -m atlas_rapporteur.src.main --mode dry-run --country france
PYTHONPATH=. python -m atlas_rapporteur.src.main --mode dry-run --trade plomberie
PYTHONPATH=. python -m atlas_rapporteur.src.main --mode dry-run --city Lyon
PYTHONPATH=. python -m atlas_rapporteur.src.dashboard
PYTHONPATH=. pytest -q atlas_rapporteur/tests
```

## Exports
- `runtime/exports/leads_ranked.json`
- `runtime/exports/leads_ranked.csv`
- `runtime/reports/daily_report.md`
- `runtime/db/atlas.db`

## Déploiement
Compatible Docker/VPS/Render/Railway/Fly.io (service worker quotidien + service web dashboard).

## Limites V0
- Connecteur Google réel à brancher selon clés (mode dry-run inclus).
- Extraction de contacts basée sur signaux disponibles dans les résultats.
- Scheduler externe recommandé (cron/GitHub Actions).
