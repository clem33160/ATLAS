# Atlas Navigation Core
- `bash atlas_governance/scripts/atlas_whereami.sh`
- `bash atlas_governance/scripts/atlas_preflight.sh`
- `bash atlas_governance/scripts/atlas_health.sh`
- `bash atlas_governance/scripts/atlas_merge_oracle.sh`

## Atlas Business MVP (Termux + external data)

Atlas Business MVP is config-driven and stores large/private data outside git in `~/atlas_data`.

### Setup
```bash
cp atlas.config.example.yaml atlas.config.yaml
mkdir -p ~/atlas_data/{wikidata,sirene,documents,indexes,secrets,imports/gmail,sandbox/proof1000}
python -m pip install -U pyyaml pytest
```

### Run proof1000 sandbox
```bash
python -c "from pathlib import Path; from core.proof.proof1000 import run_proof1000; print(run_proof1000(Path('~/atlas_data/sandbox/proof1000').expanduser()))"
```

### Run document indexing
```bash
python - <<'PY'
from pathlib import Path
from core.documents.engine import DocumentEngine
engine = DocumentEngine()
root = Path('~/atlas_data/documents').expanduser()
for p in root.glob('*.txt'):
    print(engine.index_document(p))
PY
```

### Test access control
```bash
pytest -q tests/test_atlas_business_mvp.py
```

## Pilot MVP plomberie/chauffage (contrôlé)

### Pilot-ready vs Public SaaS
- Pilot-ready: connecteurs mockables, ingestion docs, RBAC, audit chain, score readiness, dashboard local.
- Not public-SaaS-ready: isolation multi-client forte, conformité RGPD complète, UI/UX avancée, sauvegarde/restore durcie.

### Termux quick run
```bash
cp atlas.config.example.yaml atlas.config.yaml
mkdir -p ~/atlas_data/{secrets,imports/gmail,sandbox/proof1000,documents,indexes}
python -m pytest -q
./scripts/atlas proof1000
./scripts/atlas dashboard
```

### Gmail import
```bash
./scripts/atlas import-gmail --query "has:attachment filename:pdf"
```

### Readiness & sales value
```bash
./scripts/atlas readiness
./scripts/atlas value-report
```

## Canonical test suite (merge-safe)

Canonical command:
```bash
python -m pytest -q
```

Default collection is intentionally restricted to `tests/` via `pytest.ini`.
Legacy folders are ignored from canonical collection (not deleted):
- `atlas_governance/`
- `atlas_memory/`
- `atlas_knowledge_bridge/`
- `runtime/`
- old experimental folders (e.g. `experimental/`, `experiments/`)

Proof1000:
```bash
./scripts/atlas proof1000
```

Dashboard:
```bash
./scripts/atlas dashboard
```

Readiness:
```bash
./scripts/atlas readiness
```

Readiness position (honest):
- Pilot-ready: controlled local MVP only.
- Public SaaS-ready: no.
