import argparse
import json
from pathlib import Path

from .business_dashboard import write_business_dashboard
from .budget_guard import can_spend_query, register_query_cost, stop_reason_if_blocked
from .config import BASE
from .dedupe import dedupe_leads
from .feedback_loop import run_feedback_loop
from .lead_quality_gate import evaluate_result
from .models import Lead
from .query_lab import log_query_run
from .query_optimizer import build_query_candidates, select_next_queries
from .quality_oracle import aggregate_query_performance, evaluate_quality, write_quality_reports
from .reports import write_exports
from .scoring import score_lead
from .search_google_cse import google_cse_available, search_google_cse
from .source_quality import evaluate_source_quality


def _fixture_results():
    return json.loads((BASE / "data/fixtures/sample_search_results.json").read_text(encoding="utf-8"))


def run(mode="dry-run", limit=40, country=None, trade=None, city=None, with_summary=False):
    query_limit = min(limit, 20)
    queries = build_query_candidates(limit=query_limit, country=country, trade=trade, city=city)
    search_error = None
    stop_reason = None
    raw_results = []

    if mode == "google-cse":
        if not google_cse_available():
            return ([], {"mode": "google-cse", "error": "SKIPPED_NO_API_KEYS", "queries_used": 0, "estimated_cost_eur": 0.0, "stopped_by_budget": False, "results_retrieved": 0, "rejected": 0, "qualified": 0, "business_ready": 0}) if with_summary else []
        usable = []
        for q in queries:
            if can_spend_query():
                usable.append(q)
            else:
                stop_reason = stop_reason_if_blocked()
                break
        try:
            raw_results, used = search_google_cse(usable, limit=query_limit, logger_path=BASE / "runtime/audit/google_cse_queries.log")
            for i in range(used):
                register_query_cost(usable[i]["query"])
        except Exception as e:
            search_error = str(e)
            raw_results = []
    elif mode == "manual":
        from .search_manual import search_manual
        raw_results = search_manual()[:query_limit]
    else:
        raw_results = _fixture_results()[:query_limit]

    evaluated = []
    leads = []
    rejected_results = []
    for i, r in enumerate(raw_results):
        status, evidence = evaluate_result(r)
        item = {**r, "status": status, "evidence": evidence, "query": queries[min(i, len(queries)-1)]["query"] if queries else ""}
        evaluated.append(item)
        if status == "TO_VALIDATE":
            lead = Lead(title=r.get("title", ""), url=r.get("url", ""), snippet=r.get("snippet", ""), city=r.get("city", "INCERTAIN"), country=r.get("country", "INCERTAIN"), trade=r.get("trade", "INCERTAIN"), tier="TO_VALIDATE")
            leads.append(score_lead(lead))
        else:
            rejected_results.append({"url": r.get("url", ""), "title": r.get("title", ""), "reason": status, "evidence": evidence})

    leads = dedupe_leads(leads)
    leads.sort(key=lambda x: x.score, reverse=True)
    qcosts = json.loads((BASE / "runtime/audit/query_costs.json").read_text(encoding="utf-8")) if (BASE / "runtime/audit/query_costs.json").exists() else []
    budget_remaining = max(0, int(__import__("os").getenv("SEARCH_DAILY_LIMIT", "100")) - len(qcosts))
    write_exports(leads, rejected=rejected_results, query_costs=qcosts, summary={"results_retrieved": len(raw_results), "queries_used": len(raw_results), "estimated_cost_eur": round(len(raw_results) * 0.005, 3), "budget_remaining_queries": budget_remaining})

    qrows = evaluate_quality(evaluated)
    qperf = aggregate_query_performance(qrows)
    write_quality_reports(qrows, qperf)
    source_q = evaluate_source_quality(evaluated)
    fb = run_feedback_loop()
    next_q = select_next_queries(qperf, 10)
    p = BASE / "runtime/query_lab"; p.mkdir(parents=True, exist_ok=True)
    (p / "next_queries.json").write_text(json.dumps(next_q, ensure_ascii=False, indent=2), encoding="utf-8")
    log_query_run({"mode": mode, "results": len(raw_results), "rejected": len(rejected_results), "stop_reason": stop_reason})

    summary = {"mode": mode, "queries_used": len(raw_results), "results_retrieved": len(raw_results), "rejected": len(rejected_results), "qualified": len(leads), "business_ready": len([l for l in leads if l.qualification_status == "BUSINESS_READY"]), "estimated_cost_eur": round(len(raw_results) * 0.005, 3), "error": search_error, "stopped_by_budget": bool(stop_reason), "stop_reason": stop_reason, "feedback": fb}
    write_business_dashboard(leads, summary, qperf=qperf, source_quality=source_q, next_queries=next_q)
    return (leads, summary) if with_summary else leads


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--mode", default="dry-run")
    p.add_argument("--google-cse", action="store_true")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--dashboard", action="store_true")
    p.add_argument("--query-lab", action="store_true")
    p.add_argument("--manual", action="store_true")
    p.add_argument("--limit", type=int, default=40)
    p.add_argument("--country")
    p.add_argument("--trade")
    p.add_argument("--city")
    a = p.parse_args()
    mode = "manual" if a.manual else "google-cse" if a.google_cse else "dry-run" if a.dry_run else a.mode
    _, summary = run(mode=mode, limit=a.limit, country=a.country, trade=a.trade, city=a.city, with_summary=True)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
