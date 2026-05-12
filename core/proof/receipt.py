from __future__ import annotations
from datetime import datetime, UTC

def build_receipt(role: str, doc_id: str, original_path: str, delivered_path: str, sha256: str, decision: str, provenance: dict) -> dict:
    return {"role": role, "doc_id": doc_id, "original_path": original_path, "delivered_path": delivered_path, "sha256": sha256, "timestamp": datetime.now(UTC).isoformat(), "decision": decision, "provenance": provenance}
