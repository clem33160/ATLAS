import csv, json
from collections import Counter
from .config import BASE

def run_feedback_loop():
    inbox = BASE / "inbox"
    call_path = inbox / "call_updates.csv"
    human_path = inbox / "human_confirmations.csv"
    calls = []
    humans = []
    if call_path.exists():
        with call_path.open(encoding="utf-8") as f: calls = list(csv.DictReader(f))
    if human_path.exists():
        with human_path.open(encoding="utf-8") as f: humans = list(csv.DictReader(f))
    notes = "Aucun retour d’appel exploitable." if not calls else f"{len(calls)} retours d'appel lus."
    q_win = Counter([x.get("query", "") for x in calls if x.get("outcome", "").lower() in {"won", "qualified"}])
    next_q = [{"query": q, "wins": w} for q, w in q_win.most_common(10)]
    out_dir = BASE / "runtime/query_lab"; out_dir.mkdir(parents=True, exist_ok=True)
    summary = {"notes": notes, "call_updates": len(calls), "human_confirmations": len(humans)}
    (out_dir / "feedback_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    (out_dir / "winning_queries.json").write_text(json.dumps(next_q, ensure_ascii=False, indent=2), encoding="utf-8")
    (out_dir / "next_queries.json").write_text(json.dumps(next_q, ensure_ascii=False, indent=2), encoding="utf-8")
    return summary
