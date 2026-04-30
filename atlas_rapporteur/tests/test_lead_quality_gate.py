from atlas_rapporteur.src.lead_quality_gate import evaluate_result


def test_url_absente_rejet():
    s, _ = evaluate_result({"title": "x", "snippet": "cherche plomberie Lyon"})
    assert s == "REJECTED_INVALID_URL"


def test_title_vide_rejet():
    s, _ = evaluate_result({"title": "", "snippet": "cherche plomberie Lyon", "url": "https://x"})
    assert s == "REJECTED_WEAK_EVIDENCE"


def test_city_country_unknown_rejet():
    s, _ = evaluate_result({"title": "Besoin plomberie", "snippet": "cherche plomberie urgente", "url": "https://x", "city": "INCONNU", "country": "INCONNU", "trade": "INCONNU"})
    assert s == "REJECTED_INCOMPLETE_FIELDS"


def test_trade_inconnu_rejet():
    s, _ = evaluate_result({"title": "Besoin", "snippet": "cherche urgent Lyon", "url": "https://x", "city": "Lyon", "country": "FR", "trade": "INCONNU"})
    assert s == "REJECTED_INCOMPLETE_FIELDS"


def test_blog_annuaire_seller_emploi_formation_pdf_rejets():
    cases = [
        ("Blog plomberie", "blog article plomberie lyon conseils pratiques", "REJECTED_NO_CLIENT_INTENT"),
        ("Annuaire artisans", "annuaire plomberie Lyon", "REJECTED_DIRECTORY_OR_SELLER_PAGE"),
        ("Artisan nos services", "intervention 24/7", "REJECTED_DIRECTORY_OR_SELLER_PAGE"),
        ("Offre emploi plomberie Lyon", "emploi plomberie lyon urgent recrutement", "REJECTED_NO_CLIENT_INTENT"),
        ("Formation plomberie Lyon", "formation plomberie lyon certifiante", "REJECTED_NO_CLIENT_INTENT"),
    ]
    for t, sn, expected in cases:
        s, _ = evaluate_result({"title": t, "snippet": sn, "url": "https://x", "city": "Lyon", "country": "FR", "trade": "plomberie"})
        assert s == expected
    s, _ = evaluate_result({"title": "Doc", "snippet": "pdf", "url": "https://x/doc.pdf", "city": "Lyon", "country": "FR", "trade": "plomberie"})
    assert s == "REJECTED_RAW_PDF"


def test_vraie_demande_to_validate():
    s, _ = evaluate_result({"title": "cherche plombier urgent Lyon fuite", "snippet": "cherche plombier urgent Lyon fuite", "url": "https://x/need", "city": "Lyon", "country": "FR", "trade": "plomberie"})
    assert s == "TO_VALIDATE"


def test_marche_public_clair_to_validate():
    s, _ = evaluate_result({"title": "Marché public travaux plomberie Lyon", "snippet": "appel d'offres travaux plomberie Lyon", "url": "https://ville.fr/ao", "city": "Lyon", "country": "FR", "trade": "plomberie"})
    assert s == "TO_VALIDATE"
