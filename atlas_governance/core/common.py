from __future__ import annotations
import hashlib, json, os
from pathlib import Path
from datetime import datetime, timezone

FORBIDDEN_TOKENS = ["final","new","patch","copy","v2","v3","old","backup","tmp","brouillon","test_final"]

def project_root() -> Path:
    return Path(__file__).resolve().parents[2]

def governance_root() -> Path:
    return project_root()/"atlas_governance"

def runtime_dir() -> Path:
    d=governance_root()/"runtime"
    d.mkdir(parents=True, exist_ok=True)
    return d

def read_json(path: Path, default=None):
    if not path.exists():
        return {} if default is None else default
    return json.loads(path.read_text(encoding='utf-8'))

def write_json(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2)+"\n", encoding='utf-8')

def write_md(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8')

def sha256_file(path: Path) -> str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for c in iter(lambda:f.read(8192), b''):
            h.update(c)
    return h.hexdigest()

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def suspicious_name(p: str)->bool:
    l=p.lower()
    return any(t in l for t in FORBIDDEN_TOKENS)
