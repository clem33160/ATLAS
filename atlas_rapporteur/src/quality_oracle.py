import json
from collections import Counter
from .config import BASE

def evaluate_quality(results):
    rows = []
    for r in results:
        rows.append({
            "query": r.get("query", ""),
            "lead_quality_score": 80 if r.get("status") == "TO_VALIDATE" else 20,
            "rejection_reason": r.get("status") if r.get("status", "").startswith("REJECTED") else None,
            "evidence_text": r.get("evidence", ""),
            "detected_city": r.get("city", "INCERTAIN"),
            "detected_trade": r.get("trade", "INCERTAIN"),
            "detected_intent": r.get("intent", "UNKNOWN"),
            "estimated_value_band": "MEDIUM",
            "confidence": 0.8 if r.get("status") == "TO_VALIDATE" else 0.3,
            "status": r.get("status"),
        })
    return rows

def aggregate_query_performance(rows, query_cost=0.005):
    byq = {}
    for r in rows:
        q = r["query"]
        byq.setdefault(q, []).append(r)
    out = []
    for q, vals in byq.items():
        total = len(vals)
        acc = len([x for x in vals if x["status"] == "TO_VALIDATE"])
        rej = total - acc
        reasons = Counter([x["rejection_reason"] for x in vals if x["rejection_reason"]])
        rate = acc / total if total else 0
        grade = "A" if rate >= 0.7 else "B" if rate >= 0.5 else "C" if rate >= 0.3 else "D" if rate >= 0.1 else "E"
        out.append({"query": q, "total_results": total, "accepted_results": acc, "rejected_results": rej, "acceptance_rate": rate,
                    "estimated_cost": round(total * query_cost, 4), "cost_per_candidate": round(query_cost / rate, 4) if rate else None,
                    "cost_per_validated_lead": None, "top_rejection_reasons": reasons.most_common(3), "quality_grade": grade})
    return out

def write_quality_reports(rows, qperf):
    qdir = BASE / "runtime/quality"
    lab = BASE / "runtime/query_lab"
    qdir.mkdir(parents=True, exist_ok=True); lab.mkdir(parents=True, exist_ok=True)
    payload = {"results": rows, "queries": qperf}
    (qdir / "lead_quality_report.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    md = ["# Lead Quality Report", "", f"Résultats: {len(rows)}"]
    (qdir / "lead_quality_report.md").write_text("\n".join(md), encoding="utf-8")
    (lab / "query_performance.json").write_text(json.dumps(qperf, ensure_ascii=False, indent=2), encoding="utf-8")
