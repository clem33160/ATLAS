from __future__ import annotations
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterator

FORBIDDEN_TOKENS = ("v2", "final", "new", "patch", "copy", "old", "backup", "tmp")
EXCLUDE_DIRS = {".git", "__pycache__", "venv", ".venv", "node_modules"}


def repo_root(start: Path | None = None) -> Path:
    p = (start or Path.cwd()).resolve()
    for c in [p, *p.parents]:
        if (c / ".git").exists() and (c / "atlas_governance").exists():
            return c
    raise FileNotFoundError("ATLAS root not found")


def project_root() -> Path:
    return repo_root()


def governance_root() -> Path:
    return repo_root() / "atlas_governance"


def runtime_dir() -> Path:
    d = governance_root() / "runtime"
    d.mkdir(parents=True, exist_ok=True)
    return d


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_json(path: Path, default=None):
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_md(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def jread(path: Path, default=None):
    return read_json(path, default)


def jwrite(path: Path, data):
    write_json(path, data)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def suspicious_name(value: str) -> bool:
    low = value.lower()
    return any(tok in low for tok in FORBIDDEN_TOKENS)


def iter_project_files(include_runtime: bool = False) -> Iterator[Path]:
    root = repo_root()
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        rel = p.relative_to(root)
        parts = set(rel.parts)
        if EXCLUDE_DIRS & parts:
            continue
        if ("runtime" in parts) and not include_runtime:
            continue
        yield p
