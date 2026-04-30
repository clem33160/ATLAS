import json
from pathlib import Path
from .config import BASE


def load_provider_registry() -> dict:
    path = BASE / "config/providers.json"
    return json.loads(path.read_text(encoding="utf-8"))


def list_active_providers(registry: dict) -> list[dict]:
    return [p for p in registry.get("providers", []) if p.get("enabled")]


def blocked_sources(registry: dict) -> list[dict]:
    return registry.get("blocked_or_permission_required", [])


def write_provider_source_report(registry: dict, out_path: Path) -> None:
    providers = registry.get("providers", [])
    active = [p for p in providers if p.get("enabled") and p.get("legal_status") in {"active", "catalog_only"}]
    blocked = blocked_sources(registry)
    lines = [
        "# Provider Sources Report",
        "",
        f"- Providers total: {len(providers)}",
        f"- Providers actifs: {len(active)}",
        f"- Providers bloqués/révision: {len([p for p in providers if p.get('legal_status') in {'blocked_without_permission','manual_review_required','do_not_scrape'}])}",
        f"- Sources bloquées explicites: {len(blocked)}",
        "",
    ]
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines), encoding="utf-8")
