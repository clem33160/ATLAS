#!/usr/bin/env bash
set -euo pipefail

python3 -m unittest atlas.tests.test_pipeline -v
