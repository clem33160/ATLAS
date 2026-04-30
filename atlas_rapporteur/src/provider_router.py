import json
from .budget_guard import can_spend_query, register_query_cost
from .config import BASE
from .providers import BoampProvider, BraveSearchProvider, CanadaBuysProvider, CommonCrawlProvider, LegalSitemapProvider, SeaoQuebecProvider, SimapSuisseProvider, TavilySearchProvider, TedEuropeProvider


def _providers():
    return {"brave": BraveSearchProvider(), "tavily": TavilySearchProvider(), "boamp": BoampProvider(), "ted": TedEuropeProvider(), "canadabuys": CanadaBuysProvider(), "seao": SeaoQuebecProvider(), "simap": SimapSuisseProvider(), "common_crawl": CommonCrawlProvider(), "legal_sitemap": LegalSitemapProvider()}


def discover(query, selected="all", limit=10):
    cfg = json.loads((BASE / "config/providers.json").read_text(encoding="utf-8"))
    reg = _providers()
    chosen = list(reg.keys()) if selected in ("all", "discover", "official") else [selected]
    out, skipped, run_log = [], [], []
    for name in chosen:
        c = cfg.get(name, {})
        if name not in reg:
            continue
        if not c.get("enabled", False):
            skipped.append({"provider": name, "status": "SKIPPED_DISABLED", "reason": c.get("status", "disabled")})
            run_log.append({"provider": name, "query": query, "status": "SKIPPED_DISABLED", "count": 0, "error": None})
            continue
        p = reg[name]
        if not p.has_key():
            skipped.append({"provider": name, "status": "SKIPPED_NO_API_KEY"})
            run_log.append({"provider": name, "query": query, "status": "SKIPPED_NO_API_KEY", "count": 0, "error": None})
            continue
        if getattr(p, "paid", False):
            if not can_spend_query():
                skipped.append({"provider": name, "status": "SKIPPED_BUDGET_GUARD"})
                run_log.append({"provider": name, "query": query, "status": "SKIPPED_BUDGET_GUARD", "count": 0, "error": None})
                continue
            register_query_cost(f"{name}:{query}")
        rows = [r for r in p.search(query, limit=limit)[:limit] if "example.com" not in (r.get("url", ""))]
        out.extend(rows)
        run_log.append({"provider": name, "query": query, "status": "OK", "count": len(rows), "error": None})
    dedup = {r.get("url"): r for r in out if r.get("url")}
    merged = list(dedup.values())
    audit = BASE / "runtime/audit"
    audit.mkdir(parents=True, exist_ok=True)
    (audit / "provider_run_log.json").write_text(json.dumps(run_log, ensure_ascii=False, indent=2), encoding="utf-8")
    (audit / "skipped_providers.json").write_text(json.dumps(skipped, ensure_ascii=False, indent=2), encoding="utf-8")
    return merged, skipped
