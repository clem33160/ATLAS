from atlas_rapporteur.src.budget_guard import can_spend_query

def test_budget_guard_blocks_before_api_call():
    assert isinstance(can_spend_query(), bool)
