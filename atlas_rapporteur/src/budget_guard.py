import json
from datetime import date
from .config import BASE

USAGE_PATH = BASE / "runtime/audit/query_costs.json"


def _env_float(name, default):
    import os
    return float(os.getenv(name, str(default)))


def _env_int(name, default):
    import os
    return int(os.getenv(name, str(default)))


def load_usage_state():
    rows = json.loads(USAGE_PATH.read_text(encoding="utf-8")) if USAGE_PATH.exists() else []
    today = str(date.today())
    trows = [x for x in rows if x.get("day") == today]
    spent = sum(float(x.get("estimated_cost_eur", 0.0)) for x in trows)
    return {"day": today, "rows": rows, "queries_today": len(trows), "spent_today": round(spent, 6)}


def can_spend_query():
    st = load_usage_state()
    limit = _env_int("SEARCH_DAILY_LIMIT", 100)
    cost = _env_float("SEARCH_COST_PER_QUERY_EUR", 0.005)
    max_cost = limit * cost
    return st["queries_today"] < limit and (st["spent_today"] + cost) <= max_cost


def stop_reason_if_blocked():
    if can_spend_query():
        return None
    st = load_usage_state()
    limit = _env_int("SEARCH_DAILY_LIMIT", 100)
    return "max_queries_per_day_reached" if st["queries_today"] >= limit else "max_daily_cost_reached"


def register_query_cost(query):
    st = load_usage_state()
    cost = _env_float("SEARCH_COST_PER_QUERY_EUR", 0.005)
    st["rows"].append({"day": st["day"], "query": query, "estimated_cost_eur": cost})
    USAGE_PATH.parent.mkdir(parents=True, exist_ok=True)
    USAGE_PATH.write_text(json.dumps(st["rows"], ensure_ascii=False, indent=2), encoding="utf-8")
