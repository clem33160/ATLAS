from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class SourceRegistryItem:
    source_id: str
    source_type: str
    local_path: Path
    enabled: bool
    sensitivity: str
    allowed_roles: tuple[str, ...]
    provenance_rules: str
    test_status: str


def build_registry(source_rows: Iterable[dict]) -> list[SourceRegistryItem]:
    registry: list[SourceRegistryItem] = []
    for row in source_rows:
        required = {
            "source_id",
            "source_type",
            "local_path",
            "enabled",
            "sensitivity",
            "allowed_roles",
            "provenance_rules",
            "test_status",
        }
        if not required.issubset(row):
            missing = sorted(required - set(row))
            raise ValueError(f"Source row missing keys: {missing}")
        registry.append(
            SourceRegistryItem(
                source_id=row["source_id"],
                source_type=row["source_type"],
                local_path=Path(row["local_path"]).expanduser().resolve(),
                enabled=bool(row["enabled"]),
                sensitivity=row["sensitivity"],
                allowed_roles=tuple(row["allowed_roles"]),
                provenance_rules=row["provenance_rules"],
                test_status=row["test_status"],
            )
        )
    return registry
