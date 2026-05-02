#!/usr/bin/env bash
set -euo pipefail
FILE="${1:-}"
[[ -f "$FILE" ]] || { echo "Mission file not found"; exit 1; }
req=("Mission ID" "Objectif" "Domaine" "Type" "Chemins autorisés" "Chemins interdits" "Tests obligatoires" "Critères d’acceptation" "Critères de refus" "Rapport final attendu")
for r in "${req[@]}"; do grep -qi "$r" "$FILE" || { echo "Missing field: $r"; exit 1; }; done
grep -Eqi 'rm -rf|suppression massive' "$FILE" && { echo "Forbidden destructive pattern"; exit 1; }
grep -Eqi 'modification du canon sans validation' "$FILE" && { echo "Forbidden canon modification"; exit 1; }
grep -Eqi 'Objectif:\s*$|Chemins autorisés:\s*$|Chemins interdits:\s*$|Tests obligatoires:\s*$' "$FILE" && { echo "Empty critical field"; exit 1; }
echo "Mission validation OK"
