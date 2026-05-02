#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
count(){ rg --files "$@" | wc -l | tr -d " "; }
pl_files=$(count "$root/atlas/business/plomberie" "$root/atlas/sandbox/plomberie")
pl_tests=$(count "$root/tests" -g "*plomberie*test.sh")
pl_scripts=$(count "$root/scripts" -g "*plomberie*")
reports=$(count "$root/atlas/reports" -g "*PLOMBERIE*")
echo "files=$pl_files"
echo "tests=$pl_tests"
echo "scripts=$pl_scripts"
echo "reports=$reports"
