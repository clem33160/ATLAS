# Atlas Rapporteur d’Affaires V0.8 - Sources réelles et artisans vérifiables

Atlas ne garantit pas automatiquement qu’un lead est réel.
Atlas classe les leads selon preuve et source.
Pour obtenir du réel, il faut fournir de vraies URLs publiques.
Les sources privées sont désactivées par défaut.
L’humain valide toujours les CGU et la preuve.
Aucun contact automatique. Aucun scraping agressif.

```bash
cd "$HOME/atlas_workspace/ATLAS"
git pull --rebase --autostash
chmod +x ./atlas/scripts/run.sh ./atlas/scripts/test.sh ./atlas/scripts/source_audit.sh
./atlas/scripts/source_audit.sh
./atlas/scripts/test.sh
./atlas/scripts/run.sh
sed -n '1,380p' atlas/runtime/reports/lead_report.md
sed -n '1,300p' atlas/runtime/closer/daily_call_sheet.md
```
