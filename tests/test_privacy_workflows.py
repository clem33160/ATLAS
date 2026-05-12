from core.privacy.export_request import new_export_request
from core.privacy.erasure_request import new_erasure_request
from core.privacy.retention import RetentionPolicy

def test_privacy_objects():
    assert new_export_request('A','u')['type']=='export_requested'
    assert new_erasure_request('A','u')['type']=='deletion_requested'
    assert RetentionPolicy('A',365).retention_days==365
