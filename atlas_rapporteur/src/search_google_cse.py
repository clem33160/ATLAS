import json
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime

from .config import env


def google_cse_available():
    return bool(env("GOOGLE_CSE_API_KEY")) and bool(env("GOOGLE_CSE_CX"))


def _log_query(log_path, payload):
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=False) + "\n")


def search_google_cse(queries, limit=20, logger_path=None, retries=1, dry_run=False):
    key, cx = env("GOOGLE_CSE_API_KEY"), env("GOOGLE_CSE_CX")
    if (not key or not cx) and not dry_run:
        raise RuntimeError("Google CSE API keys missing")
    cost = float(env("SEARCH_COST_PER_QUERY_EUR", "0.005"))
    max_queries = min(len(queries), int(limit), int(env("SEARCH_DAILY_LIMIT", "100")))
    items, used = [], 0
    for q in queries[:max_queries]:
        start = 1
        while len(items) < limit:
            if dry_run:
                break
            params = {"key": key, "cx": cx, "q": q["query"], "num": 10, "start": start}
            url = f"https://www.googleapis.com/customsearch/v1?{urllib.parse.urlencode(params)}"
            payload=None
            for attempt in range(retries+1):
                try:
                    with urllib.request.urlopen(url, timeout=10) as r:
                        payload = json.loads(r.read().decode("utf-8"))
                    break
                except urllib.error.HTTPError as e:
                    if e.code in (429, 403):
                        raise RuntimeError("quota exceeded")
                    if attempt>=retries: raise
                except Exception:
                    if attempt>=retries: raise
            if logger_path:
                _log_query(logger_path, {"timestamp": datetime.utcnow().isoformat(), "query": q["query"], "start": start, "estimated_cost_eur": cost, "country": q.get("country"), "city": q.get("city")})
            for it in payload.get("items", []):
                items.append({"title": it.get("title", ""), "url": it.get("link", ""), "snippet": it.get("snippet", ""), "country": q.get("country", "INCONNU"), "city": q.get("city", "INCONNU"), "trade": q.get("trade", "INCONNU")})
                if len(items) >= limit:
                    break
            used += 1
            next_page = payload.get("queries", {}).get("nextPage", [])
            if not next_page:
                break
            start = int(next_page[0].get("startIndex", 0))
    return items[:limit], used
