from .config import load_json

def build_query_candidates(limit, country=None, city=None, trade=None):
    s = load_json("config/query_strategy.json")
    countries = [country] if country else s["countries"]
    trades = [trade] if trade else s["trades"]
    out = []
    for c in countries:
        for ci in s["cities_by_country"].get(c, []):
            if city and city.lower() != ci.lower():
                continue
            for t in trades:
                for pat in s["intent_patterns"]:
                    q = pat.format(trade=t, city=ci)
                    out.append({"query": q, "country": c, "city": ci, "trade": t, "score": score_query_candidate(q)})
                    if len(out) >= limit:
                        return sorted(out, key=lambda x: x["score"], reverse=True)
    return sorted(out, key=lambda x: x["score"], reverse=True)

def score_query_candidate(query):
    q = query.lower()
    s = 10
    if any(x in q for x in ["cherche", "besoin", "devis", "urgence", "travaux"]): s += 40
    if len(q.split()) >= 3: s += 20
    if any(x in q for x in ["paris", "lyon", "montréal", "genève", "luxembourg"]): s += 10
    if any(x in q for x in ["pompe à chaleur", "chaudière", "toiture", "rénovation"]): s += 10
    if len(q.split()) < 2: s -= 20
    return max(0, min(100, s))

def select_next_queries(history, limit):
    bad = {h["query"] for h in history if h.get("acceptance_rate", 0) < 0.1}
    winners = {h["query"] for h in history if h.get("acceptance_rate", 0) > 0.3}
    allq = build_query_candidates(limit * 5)
    ranked = [q for q in allq if q["query"] not in bad]
    ranked.sort(key=lambda x: (x["query"] in winners, x["score"]), reverse=True)
    return ranked[:limit]

def explain_query_choice(query):
    return "Priorisée car contient intention + métier + ville." if score_query_candidate(query) >= 60 else "Dépriorisée car trop générique."
