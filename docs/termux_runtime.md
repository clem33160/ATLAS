# Termux Runtime

## Install
```bash
pkg update && pkg upgrade -y
pkg install -y git python
python -m pip install --upgrade pip pyyaml pytest
```

## Atlas data mount
```bash
mkdir -p ~/atlas_data/{wikidata,sirene,documents,indexes,secrets,imports/gmail,sandbox/proof1000}
cp atlas.config.example.yaml atlas.config.yaml
```

Edit `atlas.config.yaml` paths if needed.

## Run
```bash
pytest -q tests/test_atlas_business_mvp.py
python -c "from pathlib import Path; from core.proof.proof1000 import run_proof1000; print(run_proof1000(Path('~/atlas_data/sandbox/proof1000').expanduser()))"
```
