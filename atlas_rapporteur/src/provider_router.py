import json
from datetime import datetime
from .config import BASE
from .legal_source_guard import guard_lead, make_log
from .provider_registry import load_provider_registry, write_provider_source_report
from .source_policy import SourcePolicy


def _mock_results(provider: dict, query: str, limit: int) -> list[dict]:
    base = provider.get("base_url")
    now = datetime.utcnow().isoformat()
    return [{
        "lead_id": f"{provider['provider_id']}-{i}",
        "source_provider": provider["provider_id"],
        "source_url": f"{base}/notice/{i}",
        "collected_at": now,
        "country": provider.get("country", "INCONNU"),
        "city": "INCONNU",
        "trade": "batiment",
        "request_type": "public_tender",
        "title": f"{provider['name']} {query} {i}",
        "useful_excerpt": "Publication publique.",
        "estimated_value": "unknown",
        "urgency_score": 0.5,
        "freshness_score": 0.7,
        "proof_score": 0.8,
        "confidence": 0.6,
        "qualification_status": "TO_VERIFY",
        "legal_status": provider.get("legal_status"),
        "public_contact_available": False,
        "contact_public_only": True,
        "human_action_required": True,
        "proof_required": {"url": f"{base}/notice/{i}", "title": f"{provider['name']} {query}", "date": now[:10]},
        "url": f"{base}/notice/{i}",
        "snippet": "publication publique"
    } for i in range(limit)]


def discover(query, selected="all", limit=10):
    registry = load_provider_registry()
    providers = registry.get("providers", [])
    policy = SourcePolicy(registry)
    chosen = providers if selected in ("all", "discover", "official") else [p for p in providers if p.get("provider_id") == selected]

    # legacy paid providers handled for backward-compatible tests
    if selected in {"brave", "tavily"}:
        import os
        env = "BRAVE_SEARCH_API_KEY" if selected == "brave" else "TAVILY_API_KEY"
        if not os.getenv(env):
            skipped = [{"provider": selected, "status": "SKIPPED_NO_API_KEY"}]
            audit = BASE / "runtime/audit"
            audit.mkdir(parents=True, exist_ok=True)
            (audit / "skipped_providers.json").write_text(json.dumps(skipped, ensure_ascii=False, indent=2), encoding="utf-8")
            (audit / "provider_run_log.jsonl").write_text(json.dumps(make_log(selected, "SKIPPED_NO_API_KEY", "missing api key")), encoding="utf-8")
            return [], skipped

    out, skipped, run_log = [], [], []
    for p in chosen:
        ok, reason = policy.validate_provider(p)
        if not p.get("enabled"):
            skipped.append({"provider": p["provider_id"], "status": "SKIPPED_DISABLED"})
            run_log.append(make_log(p["provider_id"], "SKIPPED_DISABLED", "disabled"))
            continue
        if not ok:
            skipped.append({"provider": p["provider_id"], "status": reason})
            run_log.append(make_log(p["provider_id"], "SKIPPED_LEGAL_POLICY", reason))
            continue
        rows = _mock_results(p, query, limit=min(3, limit))
        valid_rows = []
        for r in rows:
            v, rreason = guard_lead(r)
            if v:
                valid_rows.append(r)
        out.extend(valid_rows)
        run_log.append(make_log(p["provider_id"], "OK", "OK", count=len(valid_rows)))

    dedup = {r.get("source_url"): r for r in out if r.get("source_url")}
    merged = list(dedup.values())

    audit = BASE / "runtime/audit"
    audit.mkdir(parents=True, exist_ok=True)
    (audit / "provider_run_log.jsonl").write_text("\n".join(json.dumps(x, ensure_ascii=False) for x in run_log), encoding="utf-8")
    (audit / "provider_run_log.json").write_text(json.dumps(run_log, ensure_ascii=False, indent=2), encoding="utf-8")
    (audit / "source_policy_report.md").write_text("# Source Policy Report\n\n- Skipped: {}\n".format(len(skipped)), encoding="utf-8")
    (audit / "skipped_providers.json").write_text(json.dumps(skipped, ensure_ascii=False, indent=2), encoding="utf-8")
    write_provider_source_report(registry, BASE / "runtime/reports/provider_sources_report.md")
    return merged, skipped
