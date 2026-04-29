# ATLAS — Rapporteur d’Affaires (V0.5)

V0.5 transforme la démo locale en base exploitable pour un rapporteur d’affaires local, **sans scraping internet réel**.

## Principes légaux
- Aucun scraping agressif.
- Aucune connexion automatique à des services externes.
- Aucune prise de contact automatique.
- Atlas prépare des opportunités, un humain valide puis appelle.

## Nouveautés V0.5
- Inbox locale `atlas/inbox/` pour ajout manuel de leads.
- Import de leads en JSON et CSV.
- Normalisation des champs (ville, métier, budget, urgence, confiance, etc.).
- Déduplication simple (ville + métier + titre similaire + budget proche).
- Scoring /100 détaillé et catégories `PETIT`, `MOYEN`, `GROS`, `TITAN`.
- Statut pipeline (`NOUVEAU`, `À_APPELER`, `APPELÉ`, `INTÉRESSÉ`, `À_RELANCER`, `DEAL_POTENTIEL`, `SIGNÉ`, `PERDU`).
- Rapport Markdown enrichi + exports JSON/CSV + résumé d’exécution JSON.

## Workflow Codex Web + GitHub + Termux
1. Modifier via Codex Web (PR GitHub).
2. Merger la PR sur GitHub.
3. Sur Termux: pull, test, run.

## Commandes exactes
Depuis la racine du dépôt:

```bash
./atlas/scripts/test.sh
./atlas/scripts/run.sh
```

## Ajouter des leads manuels (`atlas/inbox/`)
- JSON: `atlas/inbox/leads_manual_example.json`
- CSV: `atlas/inbox/leads_manual_example.csv`

Vous pouvez dupliquer ces fichiers et ajouter vos leads. Ils seront intégrés automatiquement au prochain run.

## Sorties générées
- Rapport: `atlas/runtime/reports/lead_report.md`
- Export JSON complet: `atlas/runtime/export/leads_ranked.json`
- Export CSV complet: `atlas/runtime/export/leads_ranked.csv`
- Résumé d’exécution JSON: `atlas/runtime/outputs/run_summary.json`

## Termux (Android)
```bash
pkg update -y && pkg upgrade -y
pkg install -y git python

git clone <URL_DU_DEPOT> ATLAS
cd ATLAS

git pull --rebase --autostash
./atlas/scripts/test.sh
./atlas/scripts/run.sh
```
