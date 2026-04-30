import csv
import json
from collections import Counter
from .config import BASE


def write_exports(leads, rejected=None, query_costs=None, summary=None):
    rejected = rejected or []
    query_costs = query_costs or []
    summary = summary or {}
    exp = BASE / "runtime/exports"; rep = BASE / "runtime/reports"; closer = BASE / "runtime/closer"; audit = BASE / "runtime/audit"
    for p in (exp, rep, closer, audit):
        p.mkdir(parents=True, exist_ok=True)

    payload = [l.to_dict() for l in leads]
    accepted = [d for d in payload if d.get("qualification_status") == "TO_VALIDATE"]
    business_ready = [d for d in payload if d.get("qualification_status") == "BUSINESS_READY"]
    human_confirmed = [d for d in payload if d.get("qualification_status") == "HUMAN_CONFIRMED"]

    (exp / "leads_ranked.json").write_text(json.dumps(accepted, ensure_ascii=False, indent=2), encoding="utf-8")
    fields = ["lead_id","title","source_url","source_domain","country","city","trade","intent_type","urgency","freshness_days","budget_low","budget_mid","budget_high","budget_status","contact_phone","contact_email","contact_form","evidence_summary","raw_snippet","score","tier","qualification_status","created_at"]
    with (exp / "leads_ranked.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader()
        for d in accepted:
            w.writerow({k: d.get(k, "") for k in fields})

    report_json = {
        "accepted_to_validate": accepted,
        "rejected_results": rejected,
        "business_ready": business_ready,
        "human_confirmed": human_confirmed,
        "query_costs": query_costs,
        "summary": summary,
    }
    (rep / "daily_report.json").write_text(json.dumps(report_json, ensure_ascii=False, indent=2), encoding="utf-8")

    rejected_counter = Counter([r.get("reason", "UNKNOWN") for r in rejected]).most_common(5)
    md = ["# Rapport quotidien", "", f"- Total récupéré: {summary.get('results_retrieved', len(accepted) + len(rejected))}",
          f"- Nombre rejeté: {len(rejected)}", f"- Nombre TO_VALIDATE: {len(accepted)}", f"- Nombre BUSINESS_READY: {len(business_ready)}",
          f"- Coût estimé: {summary.get('estimated_cost_eur', 0.0)} EUR", f"- Budget restant (requêtes): {summary.get('budget_remaining_queries', 'INCONNU')}",
          f"- Requêtes utilisées: {summary.get('queries_used', 'INCONNU')}", "", "## Top 10 TO_VALIDATE", ""]
    for d in accepted[:10]:
        md.append(f"- {d['title']} | {d['city']} | {d['trade']} | {d['source_url']}")
    md += ["", "## Top bruit rejeté"]
    for reason, count in rejected_counter:
        md.append(f"- {reason}: {count}")
    (rep / "daily_report.md").write_text("\n".join(md), encoding="utf-8")

    call_now = [d for d in payload if d.get("qualification_status") in ("HUMAN_CONFIRMED", "BUSINESS_READY")]
    to_validate = accepted
    lines = ["# Closer Call Sheet", "", "## À appeler maintenant"]
    lines += [f"- {d['title']} ({d['source_url']})" for d in call_now] or ["- Aucun lead"]
    lines += ["", "## À valider"]
    for d in to_validate:
        lines.append(f"- {d['title']} | {d['city']} | {d['trade']} | {d['source_url']} | {d['evidence_summary']} | score={d['score']} | tier={d['tier']}")
    lines += ["", "## Rejetés"] + [f"- {r.get('title','')} :: {r.get('reason','')}" for r in rejected]
    (closer / "closer_call_sheet.md").write_text("\n".join(lines), encoding="utf-8")

    (audit / "rejected_results.json").write_text(json.dumps(rejected, ensure_ascii=False, indent=2), encoding="utf-8")
    (audit / "query_costs.json").write_text(json.dumps(query_costs, ensure_ascii=False, indent=2), encoding="utf-8")
