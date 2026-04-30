import json
from collections import Counter
from urllib.parse import urlparse
from .config import BASE

def evaluate_source_quality(rows):
    by = {}
    for r in rows:
        d = urlparse(r.get("url", "")).netloc or "unknown"
        by.setdefault(d, []).append(r)
    out = []
    for d, vals in by.items():
        total = len(vals)
        acc = len([v for v in vals if v.get("status") == "TO_VALIDATE"])
        rej = total - acc
        rate = acc / total if total else 0
        reasons = Counter([v.get("status") for v in vals if str(v.get("status", "")).startswith("REJECTED")])
        rec = "KEEP" if rate >= 0.5 else "WATCH" if rate >= 0.2 else "DOWNRANK" if total >= 2 else "BLOCK"
        out.append({"domain": d, "results_count": total, "accepted_count": acc, "rejected_count": rej, "acceptance_rate": rate,
                    "top_rejection_reasons": reasons.most_common(3), "recommended_action": rec})
    out.sort(key=lambda x: x["acceptance_rate"], reverse=True)
    p = BASE / "runtime/query_lab"
    p.mkdir(parents=True, exist_ok=True)
    (p / "source_quality.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    (p / "source_quality.md").write_text("# Source Quality\n", encoding="utf-8")
    return out
