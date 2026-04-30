from atlas_rapporteur.src.models import Lead
from atlas_rapporteur.src.artisan_matcher import match_artisans


def test_artisan_matcher_structured():
    lead = Lead(trade="plomberie", city="Lyon", country="France")
    lead = match_artisans(lead)
    assert isinstance(lead.matched_artisans, list)
    if lead.matched_artisans:
        a = lead.matched_artisans[0]
        for k in ["name","trade","city","country","phone","website","source_url","source_type","verification_status","confidence","match_score"]:
            assert k in a
