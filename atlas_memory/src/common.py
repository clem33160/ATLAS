from __future__ import annotations

import json
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parents[1]
RUNTIME_DIR = BASE_DIR / "runtime"

RUNTIME_PATHS = {
    "raw": RUNTIME_DIR / "raw/events.jsonl",
    "semantic": RUNTIME_DIR / "semantic/concepts.jsonl",
    "canon": RUNTIME_DIR / "canon/domains",
    "evidence": RUNTIME_DIR / "evidence/proofs.jsonl",
    "conflict": RUNTIME_DIR / "conflict/conflicts.jsonl",
    "temporal": RUNTIME_DIR / "temporal/timeline.jsonl",
    "procedures": RUNTIME_DIR / "procedures/procedures.jsonl",
    "self": RUNTIME_DIR / "self/self_state.json",
    "objectives": RUNTIME_DIR / "objectives/objectives.jsonl",
    "uncertainty": RUNTIME_DIR / "uncertainty/uncertainties.jsonl",
    "simulation": RUNTIME_DIR / "simulation/scenarios.jsonl",
    "audit": RUNTIME_DIR / "audit/audit_ledger.jsonl",
    "active": RUNTIME_DIR / "active/active_context.json",
    "index": RUNTIME_DIR / "index/global_memory_map.json",
    "health_json": RUNTIME_DIR / "reports/memory_health.json",
    "health_md": RUNTIME_DIR / "reports/memory_health.md",
    "causal": RUNTIME_DIR / "semantic/causal_links.jsonl",
    "social": RUNTIME_DIR / "self/user_preferences.json",
}

SENSITIVE_KEYS = {"ssn", "password", "token", "secret", "credit_card", "iban", "passport"}


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def new_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:12]}"


def ensure_runtime_structure() -> None:
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
