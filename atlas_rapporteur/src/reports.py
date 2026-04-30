import csv
import json
from .config import BASE


def write_exports(leads, rejected=None, query_costs=None):
    exp = BASE / "runtime/exports"
    rep = BASE / "runtime/reports"
    closer = BASE / "runtime/closer"
    audit = BASE / "runtime/audit"
    for p in (exp, rep, closer, audit):
        p.mkdir(parents=True, exist_ok=True)

    payload = [l.to_dict() for l in leads]
    (exp / "leads_ranked.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    with (exp / "leads_ranked.csv").open("w", encoding="utf-8", newline="") as f:
        fields = ["title", "url", "city", "country", "trade", "snippet", "score", "tier"]
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for d in payload:
            w.writerow({k: d.get(k, "") for k in fields})

    lines = ["# Rapport quotidien Atlas", "", "|Score|Statut|Métier|Ville|URL|", "|---:|---|---|---|---|"]
    for d in payload[:50]:
        lines.append(f"|{d['score']}|{d['tier']}|{d['trade']}|{d['city']}|{d['url']}|")
    (rep / "daily_report.md").write_text("\n".join(lines), encoding="utf-8")

    closer_lines = ["# Closer Call Sheet", "", "|Lead|Ville|Métier|Preuve|", "|---|---|---|---|"]
    for d in payload[:30]:
        closer_lines.append(f"|{d['title']}|{d['city']}|{d['trade']}|{d['snippet'][:100]}|")
    (closer / "closer_call_sheet.md").write_text("\n".join(closer_lines), encoding="utf-8")

    (audit / "query_costs.json").write_text(json.dumps(query_costs or [], ensure_ascii=False, indent=2), encoding="utf-8")
    (audit / "rejected_results.json").write_text(json.dumps(rejected or [], ensure_ascii=False, indent=2), encoding="utf-8")
