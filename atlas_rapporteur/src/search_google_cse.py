import json
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime

from .config import env, load_budget


def google_cse_available():
    return bool(env("GOOGLE_CSE_API_KEY")) and bool(env("GOOGLE_CSE_CX"))


def _log_query(log_path, payload):
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=False) + "\n")


def search_google_cse(queries, limit=20, logger_path=None, retries=2):
    key, cx = env("GOOGLE_CSE_API_KEY"), env("GOOGLE_CSE_CX")
    cost_per_query = float(env("SEARCH_COST_PER_QUERY_EUR", "0.005"))
    budget = load_budget()
    per_run_cap = min(int(limit), int(budget["max_queries_per_run"]))
    items = []
    used = 0
    start_index = 1
    log_path = logger_path

    for q in queries:
        if used >= per_run_cap or len(items) >= limit:
            break
        params = {"key": key, "cx": cx, "q": q["query"], "num": 10, "start": start_index}
        url = f"https://www.googleapis.com/customsearch/v1?{urllib.parse.urlencode(params)}"

        for attempt in range(retries + 1):
            try:
                with urllib.request.urlopen(url, timeout=10) as r:
                    payload = json.loads(r.read().decode("utf-8"))
                break
            except urllib.error.HTTPError as e:
                if e.code in (429, 403):
                    raise RuntimeError("quota exceeded")
                if attempt >= retries:
                    raise
                time.sleep(0.3 * (attempt + 1))
            except Exception:
                if attempt >= retries:
                    raise
                time.sleep(0.3 * (attempt + 1))

        used += 1
        if log_path:
            _log_query(
                log_path,
                {
                    "timestamp": datetime.utcnow().isoformat(),
                    "query": q["query"],
                    "country": q.get("country"),
                    "city": q.get("city"),
                    "trade": q.get("trade"),
                    "start": start_index,
                    "estimated_cost_eur": round(cost_per_query, 6),
                    "url": url,
                },
            )

        for it in payload.get("items", []):
            items.append(
                {
                    "title": it.get("title", ""),
                    "url": it.get("link", ""),
                    "snippet": it.get("snippet", ""),
                    "city": q.get("city", "INCERTAIN"),
                    "country": q.get("country", "INCERTAIN"),
                    "trade": q.get("trade", "INCERTAIN"),
                    "freshness_days": 3,
                }
            )
            if len(items) >= limit:
                break
        start_index = 1 if start_index >= 91 else start_index + 10

    return items[:limit], used
