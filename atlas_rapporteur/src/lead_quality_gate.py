from .config import load_json

NEG_MAP = {
    "blog": "REJECTED_BLOG",
    "emploi": "REJECTED_JOB",
    "recrutement": "REJECTED_JOB",
    "formation": "REJECTED_TRAINING",
    "annuaire": "REJECTED_DIRECTORY",
}


def evaluate_result(result):
    txt = f"{result.get('title','')} {result.get('snippet','')}".lower()
    if not result.get("url") or not result.get("title") or not result.get("snippet"):
        return "REJECTED_NO_CLIENT_INTENT", "missing mandatory fields"
    if result.get("url", "").lower().endswith(".pdf") and len(result.get("snippet", "").strip()) < 20:
        return "REJECTED_RAW_PDF", "raw pdf"
    for k, v in NEG_MAP.items():
        if k in txt:
            return v, f"contains {k}"
    strategy = load_json("config/query_strategy.json")
    cities = {c.lower() for v in strategy["cities_by_country"].values() for c in v}
    trades = {t.lower() for t in strategy["trades"]}
    if not any(c in txt for c in cities):
        return "REJECTED_NO_CITY", "city not found"
    if not any(t in txt for t in trades):
        return "REJECTED_NO_TRADE", "trade not found"
    if not any(i in txt for i in ["cherche", "besoin", "devis", "urgence", "travaux", "fuite", "panne", "remplacement", "rénovation"]):
        return "REJECTED_NO_CLIENT_INTENT", "intent not found"
    return "TO_VALIDATE", "client intent probable"
