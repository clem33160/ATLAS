from atlas_rapporteur.src.search_google_cse import google_cse_available

def test_google_cse_availability_bool():
    assert isinstance(google_cse_available(), bool)
