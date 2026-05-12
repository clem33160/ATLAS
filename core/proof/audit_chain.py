from __future__ import annotations
import hashlib
import json

EVENT_TYPES = {"import","classify","index","search","ambiguous_refusal","delivery","access_denied","hash_changed_refusal","token_refresh","OCR_attempt"}

class AuditChain:
    def __init__(self) -> None:
        self.events: list[dict] = []
    def append(self, event_type: str, payload: dict) -> dict:
        if event_type not in EVENT_TYPES:
            raise ValueError("unsupported event")
        prev = self.events[-1]["current_hash"] if self.events else "GENESIS"
        base = {"event_type": event_type, "payload": payload, "previous_hash": prev}
        raw = json.dumps(base, sort_keys=True).encode()
        current = hashlib.sha256(raw).hexdigest()
        base["current_hash"] = current
        self.events.append(base)
        return base
    def verify(self) -> bool:
        prev = "GENESIS"
        for e in self.events:
            base = {"event_type": e["event_type"], "payload": e["payload"], "previous_hash": prev}
            if hashlib.sha256(json.dumps(base, sort_keys=True).encode()).hexdigest() != e["current_hash"]:
                return False
            prev = e["current_hash"]
        return True
