from __future__ import annotations

import json
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parents[1]
DEFAULT_RUNTIME_DIR = BASE_DIR / "runtime"


def get_runtime_dir() -> Path:
    override = os.environ.get("ATLAS_MEMORY_RUNTIME_DIR", "").strip()
    return Path(override).resolve() if override else DEFAULT_RUNTIME_DIR


def _build_runtime_paths(runtime_dir: Path) -> dict[str, Path]:
    return {
        "raw": runtime_dir / "raw/events.jsonl",
        "semantic": runtime_dir / "semantic/concepts.jsonl",
        "canon": runtime_dir / "canon/domains",
        "evidence": runtime_dir / "evidence/proofs.jsonl",
        "conflict": runtime_dir / "conflict/conflicts.jsonl",
        "temporal": runtime_dir / "temporal/timeline.jsonl",
        "procedures": runtime_dir / "procedures/procedures.jsonl",
        "self": runtime_dir / "self/self_state.json",
        "objectives": runtime_dir / "objectives/objectives.jsonl",
        "uncertainty": runtime_dir / "uncertainty/uncertainties.jsonl",
        "simulation": runtime_dir / "simulation/scenarios.jsonl",
        "audit": runtime_dir / "audit/audit_ledger.jsonl",
        "active": runtime_dir / "active/active_context.json",
        "index": runtime_dir / "index/global_memory_map.json",
        "health_json": runtime_dir / "reports/memory_health.json",
        "health_md": runtime_dir / "reports/memory_health.md",
        "causal": runtime_dir / "semantic/causal_links.jsonl",
        "social": runtime_dir / "self/user_preferences.json",
    }


RUNTIME_PATHS: dict[str, Path] = _build_runtime_paths(get_runtime_dir())


def refresh_runtime_paths() -> None:
    RUNTIME_PATHS.clear()
    RUNTIME_PATHS.update(_build_runtime_paths(get_runtime_dir()))


SENSITIVE_KEYS = {"ssn", "password", "token", "secret", "credit_card", "iban", "passport"}


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def new_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:12]}"


def ensure_runtime_structure() -> None:
    refresh_runtime_paths()
    for path in RUNTIME_PATHS.values():
        path.parent.mkdir(parents=True, exist_ok=True)
    for key, path in RUNTIME_PATHS.items():
        if path.suffix in {".jsonl", ".json"} and not path.exists():
            if path.suffix == ".json":
                path.write_text("{}", encoding="utf-8")
            else:
                path.write_text("", encoding="utf-8")
    RUNTIME_PATHS["canon"].mkdir(parents=True, exist_ok=True)


def append_jsonl(path: Path, payload: dict[str, Any]) -> None:
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False) + "\n")


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def has_sensitive_data(item: dict[str, Any]) -> bool:
    lower = json.dumps(item, ensure_ascii=False).lower()
    return any(key in lower for key in SENSITIVE_KEYS)
