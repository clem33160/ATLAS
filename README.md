# Atlas Rapporteur d’Affaires (V0.6)

Atlas V0.6 est une base locale et légale de rapporteur d’affaires.

## Cadre légal
- Pas de spam, pas de contact automatique, pas de bypass captcha/login/ToS.
- Humain dans la boucle: Atlas prépare, l’humain valide et appelle.
- Les vraies sources externes sont **désactivées par défaut** (`atlas/config/sources.yaml`).

## V0.6
- Registre de sources publiques légales.
- Collecte semi-automatique contrôlée via `atlas/inbox/source_urls.txt`.
- Preuves (URL/date/extrait/confiance) et journal evidence.
- Qualification lead enrichie + scoring économique /100.
- Matching artisans renforcé + fallback humain.
- Mini CRM local + suivi des appels CSV.
- Exports closer (`atlas/runtime/closer/`).
- Rapport Markdown V0.6 lisible.

## Termux
```bash
pkg update -y && pkg upgrade -y
pkg install -y git python

git clone <URL_DU_DEPOT> ATLAS
cd ATLAS
chmod +x ./atlas/scripts/run.sh ./atlas/scripts/test.sh
./atlas/scripts/test.sh
./atlas/scripts/run.sh
```

## Workflow Codex Web + GitHub + Termux
1. Modifier via Codex Web.
2. Commit/PR GitHub.
3. Pull sur Termux.
4. `./atlas/scripts/test.sh` puis `./atlas/scripts/run.sh`.
