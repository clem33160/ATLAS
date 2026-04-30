import argparse
import json
from datetime import date

from .compliance import is_potential_lead
from .config import BASE, load_budget, settings
from .db import get_db, init_db
from .dedupe import dedupe_leads
from .models import Lead
from .query_builder import build_queries
from .reports import write_exports
from .scoring import score_lead
from .search_google_cse import google_cse_available, search_google_cse


def _fixture_results():
    return json.loads((BASE / "data/fixtures/sample_search_results.json").read_text(encoding="utf-8"))


def _daily_usage():
    with get_db() as con:
        row = con.execute("select coalesce(sum(queries),0), coalesce(sum(cost_eur),0) from budget_usage where day=?", (str(date.today()),)).fetchone()
    return int(row[0]), float(row[1])


def run(mode="dry-run", limit=40, country=None, trade=None, city=None, with_summary=False):
    init_db()
    cfg = settings()
    budget = load_budget()
    query_limit = min(limit, cfg["daily_limit"], budget["max_queries_per_run"])
    queries = build_queries(limit=query_limit, country=country, trade=trade, city=city)
    search_error = None
    stopped_by_budget = False
    rejected_results = []
    query_costs = []

    if mode == "google-cse":
        if not google_cse_available():
            mode = "dry-run"
        else:
            used_today, cost_today = _daily_usage()
            if used_today >= budget["max_queries_per_day"] or cost_today >= budget["max_daily_cost_eur"]:
                stopped_by_budget = True
                results = []
            else:
                allowed = min(query_limit, budget["max_queries_per_day"] - used_today)
                max_by_cost = int((budget["max_daily_cost_eur"] - cost_today) / cfg["cost_per_query_eur"])
                allowed = min(allowed, max(0, max_by_cost))
                if allowed <= 0:
                    stopped_by_budget = True
                    results = []
                else:
                    try:
                        results, used = search_google_cse(
                            queries[:allowed],
                            limit=query_limit,
                            logger_path=BASE / "runtime/audit/google_cse_queries.log",
                        )
                        for i in range(used):
                            query_costs.append({"query": queries[i]["query"], "estimated_cost_eur": cfg["cost_per_query_eur"]})
                    except Exception as e:
                        search_error = str(e)
                        results = []
    if mode == "dry-run":
        results = _fixture_results()

    leads = []
    for r in results[:query_limit]:
        lead = Lead(
            title=r.get("title", ""),
            url=r.get("url", ""),
            snippet=r.get("snippet", ""),
            city=r.get("city", "INCERTAIN"),
            country=r.get("country", "INCERTAIN"),
            trade=r.get("trade", "INCERTAIN"),
            freshness_days=int(r.get("freshness_days", 3)),
            urgency="URGENT" if "urgent" in r.get("snippet", "").lower() else "NORMAL",
            contact_phone=r.get("contact_phone", "ABSENT"),
            contact_email=r.get("contact_email", "ABSENT"),
            contact_form=r.get("contact_form", "ABSENT"),
            tier="TO_VALIDATE",
        )
        if is_potential_lead(lead):
            leads.append(score_lead(lead))
        else:
            rejected_results.append({"url": lead.url, "title": lead.title, "reasons": lead.rejection_reasons})
    leads = dedupe_leads(leads)
    leads.sort(key=lambda x: x.score, reverse=True)
    write_exports(leads, rejected=rejected_results, query_costs=query_costs)

    used_queries = len(query_costs)
    if used_queries:
        with get_db() as con:
            con.execute("insert or replace into budget_usage(day,queries,cost_eur) values(?,?,?)", (str(date.today()), used_queries, round(used_queries * cfg["cost_per_query_eur"], 3)))

    summary = {
        "mode": mode,
        "queries_used": used_queries,
        "results_retrieved": len(results),
        "rejected": len(rejected_results),
        "qualified": len(leads),
        "estimated_cost_eur": round(used_queries * cfg["cost_per_query_eur"], 3),
        "error": search_error,
        "stopped_by_budget": stopped_by_budget,
    }
    return (leads, summary) if with_summary else leads


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--mode", default="dry-run")
    p.add_argument("--google-cse", action="store_true")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--limit", type=int, default=40)
    p.add_argument("--country")
    p.add_argument("--trade")
    p.add_argument("--city")
    a = p.parse_args()
    mode = "google-cse" if a.google_cse else "dry-run" if a.dry_run else a.mode
    _, summary = run(mode=mode, limit=a.limit, country=a.country, trade=a.trade, city=a.city, with_summary=True)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
