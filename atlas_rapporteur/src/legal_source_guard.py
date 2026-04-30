from datetime import datetime


REQUIRED_LEAD_FIELDS = [
    "source_url",
    "proof_required",
]


def guard_lead(lead: dict) -> tuple[bool, str]:
    if not lead.get("source_url"):
        return False, "REJECTED_NO_SOURCE_URL"
    if not lead.get("proof_required"):
        return False, "REJECTED_NO_PROOF"
    if lead.get("qualification_status") == "BUSINESS_READY" and not lead.get("human_action_required"):
        return False, "REJECTED_NO_HUMAN_VALIDATION"
    return True, "OK"


def make_log(provider_id: str, status: str, reason: str, count: int = 0) -> dict:
    return {
        "provider_id": provider_id,
        "status": status,
        "reason": reason,
        "count": count,
        "timestamp": datetime.utcnow().isoformat(),
    }
