from core.access.checks import can_access

def test_access_rules():
    assert can_access('owner','invoice')
    assert not can_access('apprentice','invoice')
    assert can_access('external_client','client_doc','c1','c1')
    assert not can_access('external_client','client_doc','c1','c2')
