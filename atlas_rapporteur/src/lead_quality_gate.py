from urllib.parse import urlparse

from .query_builder import load_strategy

BLOCKED_DOMAINS = {"google.com", "www.google.com", "boamp.fr", "www.boamp.fr"}
NEGATIVE = ["blog", "annuaire", "emploi", "recrutement", "formation", "wikipedia"]
SELLER_TOKENS = ["nos services", "intervention 24/7", "artisan", "dépannage"]
INTENT_TOKENS = ["cherche", "besoin", "devis", "urgence", "fuite", "panne", "travaux", "appel d'offres", "marché public"]


def evaluate_result(result):
    title = (result.get("title") or "").strip()
    snippet = (result.get("snippet") or "").strip()
    url = (result.get("url") or "").strip()
    city = (result.get("city") or "INCONNU").strip()
    country = (result.get("country") or "INCONNU").strip()
    trade = (result.get("trade") or "INCONNU").strip()
    source_domain = urlparse(url).netloc.lower()
    text = f"{title} {snippet}".lower()

    if not url.startswith(("http://", "https://")):
        return "REJECTED_INVALID_URL", "source_url manquante ou invalide"
    if not title:
        return "REJECTED_WEAK_EVIDENCE", "title vide"
    if url.lower().endswith(".pdf") and len(snippet) < 25:
        return "REJECTED_RAW_PDF", "pdf brut illisible"
    if len(snippet) < 15:
        return "REJECTED_WEAK_EVIDENCE", "snippet trop faible"
    if source_domain in BLOCKED_DOMAINS:
        return "REJECTED_BLOCKED_SOURCE_DOMAIN", source_domain

    if any(tok in text for tok in NEGATIVE):
        if "annuaire" in text:
            return "REJECTED_DIRECTORY_OR_SELLER_PAGE", "annuaire simple"
        return "REJECTED_NO_CLIENT_INTENT", "source non business"

    if any(tok in text for tok in SELLER_TOKENS) and not any(tok in text for tok in ["cherche", "besoin", "devis"]):
        return "REJECTED_DIRECTORY_OR_SELLER_PAGE", "page vendeur artisan"

    strategy = load_strategy()
    cities = {c.lower() for vals in strategy["cities_by_country"].values() for c in vals}
    trades = {t.lower() for t in strategy["trades"]}

    city_found = city.lower() in cities or any(c in text for c in cities)
    country_found = country != "INCONNU"
    trade_found = trade.lower() in trades or any(t in text for t in trades)
    intent_found = any(i in text for i in INTENT_TOKENS)

    if not city_found and not country_found and trade == "INCONNU":
        return "REJECTED_INCOMPLETE_FIELDS", "city/country et trade inconnus"
    if not city_found and not country_found:
        return "REJECTED_INCOMPLETE_FIELDS", "localisation absente"
    if not trade_found:
        return "REJECTED_INCOMPLETE_FIELDS", "trade absent"
    if not intent_found:
        return "REJECTED_NO_CLIENT_INTENT", "intention client absente"

    return "TO_VALIDATE", "preuve textuelle suffisante"
