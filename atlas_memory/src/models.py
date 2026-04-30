from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class MemoryEvent:
    event_id: str
    created_at: str
    kind: str
    domain: str
    content: str
    source: str
    source_url: str | None
    confidence: float
    evidence_ids: list[str] = field(default_factory=list)
    linked_objective_ids: list[str] = field(default_factory=list)
    validated_by_human: bool = False
    risk_level: str = "LOW"
    useful_for_future: bool = True
    status: str = "RAW"
    tags: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__.copy()
