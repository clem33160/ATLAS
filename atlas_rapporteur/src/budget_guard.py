import json
from datetime import date
from .config import BASE, load_budget

USAGE_PATH = BASE / "runtime/audit/query_costs.json"


def load_budget_config():
    return load_budget()


def load_usage_state():
    if USAGE_PATH.exists():
        data = json.loads(USAGE_PATH.read_text(encoding="utf-8"))
    else:
        data = []
    today = str(date.today())
    today_rows = [x for x in data if x.get("day") == today]
    queries = len(today_rows)
    spent = sum(float(x.get("estimated_cost_eur", 0.0)) for x in today_rows)
    return {"day": today, "queries_today": queries, "spent_today": round(spent, 6), "rows": data}


def can_spend_query():
    cfg = load_budget_config()
    state = load_usage_state()
    if state["queries_today"] >= int(cfg["max_queries_per_day"]):
        return False
    if state["spent_today"] + float(cfg["cost_per_query_eur"]) > float(cfg["max_daily_cost_eur"]):
        return False
    return True


def stop_reason_if_blocked():
    if can_spend_query():
        return None
    cfg = load_budget_config()
    state = load_usage_state()
    if state["queries_today"] >= int(cfg["max_queries_per_day"]):
        return "max_queries_per_day_reached"
    return "max_daily_cost_reached"


def register_query_cost(query):
    cfg = load_budget_config()
    state = load_usage_state()
    state["rows"].append({
        "day": state["day"],
        "query": query,
        "estimated_cost_eur": float(cfg["cost_per_query_eur"]),
    })
    USAGE_PATH.parent.mkdir(parents=True, exist_ok=True)
    USAGE_PATH.write_text(json.dumps(state["rows"], ensure_ascii=False, indent=2), encoding="utf-8")
