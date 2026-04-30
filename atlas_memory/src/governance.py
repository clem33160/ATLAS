from __future__ import annotations
from typing import Any
from .common import has_sensitive_data

def enforce_consent(item: dict[str, Any]) -> bool:
    return bool(item.get('consent', True))

def enforce_no_sensitive_data(item: dict[str, Any]) -> bool:
    return not has_sensitive_data(item)

def enforce_privacy_rules(item: dict[str, Any]) -> bool:
    return enforce_consent(item) and enforce_no_sensitive_data(item)

def validate_memory_write(item: dict[str, Any]) -> tuple[bool,str]:
    if not enforce_consent(item):
        return False, 'CONSENT_REQUIRED'
    if not enforce_no_sensitive_data(item):
        return False, 'SENSITIVE_DATA_BLOCKED'
    return True, 'ALLOWED'

def explain_governance_decision(item: dict[str, Any]) -> dict[str, Any]:
    ok, reason=validate_memory_write(item)
    return {'allowed':ok,'reason':reason,'consent':item.get('consent',True)}
