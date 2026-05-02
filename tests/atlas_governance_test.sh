#!/usr/bin/env bash
set -euo pipefail
req=(atlas/governance/vision/ATLAS_MASTER_VISION.md atlas/governance/vision/ATLAS_OBJECTIVE.md atlas/governance/vision/ATLAS_EXECUTIVE_DOCTRINE.md atlas/governance/vision/ATLAS_INVARIANTS.md atlas/governance/vision/ATLAS_BRANCHES.md atlas/governance/vision/ATLAS_ROADMAP.md atlas/governance/canon/CANON_RULES.md atlas/governance/canon/CANON_REGISTRY.md)
for f in "${req[@]}"; do [[ -f "$f" ]] || { echo "Missing: $f"; exit 1; }; done

VISION_FILE="atlas/governance/vision/ATLAS_MASTER_VISION.md"

grep -Fq "## Résumé opérationnel" "$VISION_FILE" || { echo "Missing section: Résumé opérationnel"; exit 1; }
grep -Fq "## Source intégrale brute — Vision Atlas V0" "$VISION_FILE" || { echo "Missing section: Source intégrale brute — Vision Atlas V0"; exit 1; }

if grep -Eqi 'COLLER ICI|placeholder|à remplacer' "$VISION_FILE"; then
  echo "Canonical vision contains forbidden placeholder markers"
  exit 1
fi

word_count=$(wc -w < "$VISION_FILE")
if [[ "$word_count" -lt 4000 ]]; then
  echo "Canonical vision too short ($word_count words)"
  exit 1
fi

required_phrases=(
  "Atlas n’est pas une application"
  "infrastructure d’intelligence universelle"
  "Ne perds pas la mémoire"
  "Ne casse pas le canon"
  "Atlas Industries"
  "Atlas World Simulation"
  "Atlas Codex Bridge"
  "Le passage de la vision à l’avenir construit"
)
for phrase in "${required_phrases[@]}"; do
  grep -Fq "$phrase" "$VISION_FILE" || { echo "Missing mandatory phrase: $phrase"; exit 1; }
done

echo "governance test OK"
