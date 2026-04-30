# Atlas Rapporteur d’Affaires V0.11 — Verrouillage canonique qualité

La V0.11 verrouille la base : architecture canonique, qualité vérifiable, non-invention, stabilité Termux.

- V0.11 **n’ajoute pas de grosse nouvelle fonctionnalité**.
- Atlas **ne produit pas encore automatiquement 50 vrais leads/jour**.
- **50 leads/jour** reste un objectif futur.
- Un business 10/10 exige : vraies URLs précises, preuves exploitables, artisans vérifiables, retours d’appels, validations humaines.
- Les données DEMO ne doivent jamais être appelées ni vendues comme réelles.
- Atlas ne contacte personne automatiquement.
- Atlas ne spamme pas.
- Atlas ne contourne pas les protections.
- Atlas prépare seulement les opportunités.

## Règles anti-faux réel

- Aucun lead DEMO en `BUSINESS_READY`.
- Aucun domaine `example.org`, `example.local`, `example.com` en preuve réelle.
- Aucun `HUMAN_CONFIRMED` sans action CRM humaine.

## Ajouter des URLs publiques

Éditer `atlas/inbox/source_urls.txt` (format `source_id|url|note` ou `url`).

## Ajouter des artisans vérifiables

Utiliser des fiches artisan avec URL vérifiable (source officielle/annuaire pro) dans `atlas/inbox/`.

## Validation humaine (gate À valider → BUSINESS_READY)

- Fichier d’entrée : `atlas/inbox/human_confirmations.csv`
- Exemple : `atlas/inbox/human_confirmations.example.csv`
- Colonnes : `lead_id,confirmed_at,reviewer,decision,evidence_checked,artisan_checked,consent_status,notes`
- Un lead passe en `BUSINESS_READY` seulement si la ligne confirme :
  - `decision=CONFIRM_BUSINESS_READY`
  - `evidence_checked=yes`
  - `artisan_checked=yes`
  - `consent_status` ∈ `NON_DEMANDÉ`, `ACCORD_TRANSMISSION`, `À_CLARIFIER`
  - lead existant, non `DEMO`, avec `source_url` et au moins un artisan non-DEMO vérifiable disponible.
- Si validé : `reality_status=HUMAN_CONFIRMED`, `qualification_status=BUSINESS_READY`, `pipeline_status=À_APPELER`.
- Sinon : le lead reste `À valider` avec motif explicite dans le rapport.

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
sed -n '1,240p' atlas/runtime/audit/quality_audit.md
```

## Atlas Navigation Core
- `bash atlas_governance/scripts/atlas_whereami.sh`
- `bash atlas_governance/scripts/atlas_preflight.sh`
- `bash atlas_governance/scripts/atlas_health.sh`
- `bash atlas_governance/scripts/atlas_merge_oracle.sh`
