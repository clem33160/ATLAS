from itertools import product

TRADES = ["plombier", "chauffagiste", "serrurier", "toiture", "rénovation"]
CITIES = {
    "france": ["Paris", "Lyon", "Marseille", "Lille", "Toulouse"],
}
INTENTS = [
    "cherche {trade} fuite {city}",
    "demande devis rénovation toiture {city}",
    "besoin chauffagiste remplacement chaudière {city}",
    "travaux rénovation appartement {city} devis",
    "urgence serrure bloquée {city}",
]


def build_queries(limit=80, country=None, trade=None, city=None):
    countries = [country] if country else list(CITIES.keys())
    trades = [trade] if trade else TRADES
    queries = []
    for c in countries:
        for t, ci, pat in product(trades, CITIES.get(c, []), INTENTS):
            if city and ci.lower() != city.lower():
                continue
            queries.append({"query": pat.format(trade=t, city=ci), "country": c, "trade": t, "city": ci})
            if len(queries) >= limit:
                return queries
    return queries
