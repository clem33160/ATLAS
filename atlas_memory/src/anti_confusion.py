from __future__ import annotations

from pathlib import Path
from .common import get_runtime_dir, write_json

FORBIDDEN_TOKENS = ("final", "tmp", "backup", "copy", "old", "new")


def run_anti_confusion_scan(repo_root: Path | None = None) -> dict:
    root = (repo_root or Path.cwd()).resolve()
    ambiguous = []
    fragile_paths = []
    orphan_modules = []

    for path in root.rglob("*.py"):
        rel = path.relative_to(root)
        low_name = path.name.lower()
        if any(tok in low_name for tok in FORBIDDEN_TOKENS):
            ambiguous.append(str(rel))
        if "//" in str(rel) or ".." in str(rel):
            fragile_paths.append(str(rel))
        if path.name != "__init__.py" and path.stat().st_size < 20:
            orphan_modules.append(str(rel))

    out = {
        "ambiguous_files": sorted(ambiguous),
        "forbidden_name_hits": len(ambiguous),
        "fragile_paths": sorted(fragile_paths),
        "orphan_modules": sorted(orphan_modules),
        "ok": len(ambiguous) == 0 and len(fragile_paths) == 0,
    }
    out_path = get_runtime_dir() / "reports" / "anti_confusion_report.json"
    write_json(out_path, out)
    return out
