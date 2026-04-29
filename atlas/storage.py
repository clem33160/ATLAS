from __future__ import annotations
import csv
import json
from pathlib import Path


def ensure_runtime_dirs(base: Path) -> dict[str, Path]:
    runtime = base / "runtime"
    paths = {name: runtime / name for name in ["reports", "export", "closer", "crm", "matching", "evidence", "artisans", "business", "audit"]}
    for p in paths.values():
        p.mkdir(parents=True, exist_ok=True)
    return {"runtime": runtime, **paths}


def write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def read_json(path: Path, default: object) -> object:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def write_markdown(path: Path, content: str) -> None:
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({name: row.get(name, "") for name in fieldnames})
