from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os


@dataclass(frozen=True)
class AtlasPaths:
    wikidata_dump: Path
    sirene_data: Path
    document_root: Path
    indexes_path: Path
    google_token_path: Path
    gmail_import_path: Path
    sandbox_test_path: Path


def _expand(value: str) -> Path:
    return Path(os.path.expanduser(value)).resolve()


def load_paths(config_file: str | Path) -> AtlasPaths:
    from core.config.miniyaml import load_simple_yaml
    payload = load_simple_yaml(config_file) or {}
    paths = payload.get("paths", {})
    required = [
        "wikidata_dump",
        "sirene_data",
        "document_root",
        "indexes_path",
        "google_token_path",
        "gmail_import_path",
        "sandbox_test_path",
    ]
    missing = [key for key in required if key not in paths]
    if missing:
        raise ValueError(f"Missing required path keys: {missing}")
    return AtlasPaths(**{key: _expand(paths[key]) for key in required})
