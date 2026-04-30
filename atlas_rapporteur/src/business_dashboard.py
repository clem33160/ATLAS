import json
from collections import Counter
from .config import BASE

def write_business_dashboard(leads, summary, qperf=None, source_quality=None, next_queries=None):
    d = BASE / "runtime/dashboard"; d.mkdir(parents=True, exist_ok=True)
    tiers = Counter([l.tier for l in leads])
    payload = {
        "score_business_readiness": round((tiers.get("HUMAN_CONFIRMED", 0) + tiers.get("BUSINESS_READY", 0)) / max(1, len(leads)) * 100, 2),
        "queries_used": summary.get("queries_used", 0),
        "estimated_run_cost": summary.get("estimated_cost_eur", 0.0),
        "leads_rejected": summary.get("rejected", 0),
        "leads_to_validate": tiers.get("TO_VALIDATE", 0),
        "leads_human_confirmed": tiers.get("HUMAN_CONFIRMED", 0),
        "leads_business_ready": tiers.get("BUSINESS_READY", 0),
        "top_10_winning_queries": (qperf or [])[:10],
        "top_10_next_queries": (next_queries or [])[:10],
    }
    (d / "business_dashboard.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    (d / "business_dashboard.md").write_text("# Business Dashboard\n", encoding="utf-8")
