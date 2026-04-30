import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]


def load_strategy():
    return json.loads((BASE / "config/query_strategy.json").read_text(encoding="utf-8"))


def build_queries(limit=80, country=None, trade=None, city=None):
    s = load_strategy()
    trades = [trade] if trade else s["trades"]
    countries = [country] if country else s["priority_countries"]
    patterns = s["patterns"]
    out = []
    for c in countries:
        cities = s["cities_by_country"].get(c, [])
        for t in trades:
            for pat in patterns:
                if "{city}" in pat:
                    for ci in cities:
                        if city and ci.lower() != city.lower():
                            continue
                        out.append({"query": pat.format(trade=t, city=ci, country=c), "country": c, "city": ci, "trade": t})
                else:
                    out.append({"query": pat.format(trade=t, country=c), "country": c, "city": city or "INCONNU", "trade": t})
                if len(out) >= limit:
                    return out
    return out
