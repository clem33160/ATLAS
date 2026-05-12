from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib


@dataclass(frozen=True)
class IdentifierRecord:
    identifier_type: str
    identifier_value: str
    country: str
    jurisdiction: str
    source_id: str
    provenance: str
    confidence: float
    last_seen_at: str


def normalize_identifier_value(identifier_type: str, value: str) -> str:
    v = "".join(ch for ch in value.upper().strip() if ch.isalnum())
    return f"{identifier_type.lower()}:{v}"


def build_identifier(**kwargs: str | float) -> IdentifierRecord:
    assert kwargs.get("provenance"), "provenance required"
    assert kwargs.get("confidence") is not None, "confidence required"
    payload = dict(kwargs)
    payload["identifier_value"] = normalize_identifier_value(str(kwargs["identifier_type"]), str(kwargs["identifier_value"]))
    payload.setdefault("last_seen_at", datetime.now(timezone.utc).isoformat())
    return IdentifierRecord(**payload)  # type: ignore[arg-type]


def has_duplicate_identifiers(records: list[IdentifierRecord]) -> bool:
    seen = set()
    for r in records:
        key = (r.identifier_type, r.identifier_value, r.country, r.jurisdiction)
        if key in seen:
            return True
        seen.add(key)
    return False


def global_atlas_entity_id(seed: str) -> str:
    return "gae_" + hashlib.sha256(seed.encode("utf-8")).hexdigest()[:24]


def global_atlas_person_id(seed: str) -> str:
    return "gap_" + hashlib.sha256(seed.encode("utf-8")).hexdigest()[:24]
