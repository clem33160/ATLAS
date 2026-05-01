#!/usr/bin/env bash
set -euo pipefail
TARGETS="atlas_rapporteur_v1/core atlas_rapporteur_v1/connectors atlas_rapporteur_v1/scripts atlas_rapporteur_v1/runtime"
PAT1='s[k]-[A-Za-z0-9]+'
PAT2='s[k]-proj-[A-Za-z0-9]+'
PAT3='OPENAI'"_"'API'"_"'KEY\s*='
! rg -n "$PAT1" $TARGETS
! rg -n "$PAT2" $TARGETS
! rg -n "$PAT3" $TARGETS
! rg -n '\.''zim$' atlas_rapporteur_v1
test -z "$(git ls-files atlas_rapporteur_v1/runtime)"
