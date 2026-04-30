from __future__ import annotations

from .common import RUNTIME_PATHS, append_jsonl, now_iso, read_jsonl


def log_action(action: str, domain: str, reason: str, files=None, evidence=None, status: str = "OK") -> dict:
    payload = {"created_at": now_iso(), "action": action, "domain": domain, "reason": reason, "files": files or [], "evidence": evidence or [], "status": status}
    append_jsonl(RUNTIME_PATHS["audit"], payload)
    return payload


def list_audit(limit: int = 50) -> list[dict]:
    return read_jsonl(RUNTIME_PATHS["audit"])[-limit:]
