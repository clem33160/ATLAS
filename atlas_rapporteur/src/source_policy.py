from .provider_registry import blocked_sources

ALLOWED_SOURCE_TYPES = {
    "OPEN_DATA_API",
    "OPEN_DATA_CATALOG",
    "OPEN_DATA_DATASET",
    "OPEN_DATA_JSON",
    "PUBLIC_PROCUREMENT_PORTAL",
}


class SourcePolicy:
    def __init__(self, registry: dict):
        self.registry = registry

    def is_blocked_name(self, provider_id: str) -> bool:
        return any(s.get("provider_id") == provider_id for s in blocked_sources(self.registry))

    def validate_provider(self, provider: dict) -> tuple[bool, str]:
        if provider.get("source_type") not in ALLOWED_SOURCE_TYPES:
            return False, "SKIPPED_LEGAL_POLICY:source_type"
        if provider.get("legal_status") in {"blocked_without_permission", "do_not_scrape"}:
            return False, "SKIPPED_LEGAL_POLICY:blocked"
        if provider.get("requires_permission") and provider.get("legal_status") != "active":
            return False, "SKIPPED_LEGAL_POLICY:permission_required"
        if "captcha_bypass" in provider.get("forbidden_modes", []):
            return False, "SKIPPED_LEGAL_POLICY:captcha"
        if "forced_login" in provider.get("forbidden_modes", []):
            return False, "SKIPPED_LEGAL_POLICY:login_forced"
        return True, "OK"
