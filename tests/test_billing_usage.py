from core.billing.usage import UsageLedger

def test_usage_quota():
    u=UsageLedger(); u.add('A','documents_imported',5001)
    q=u.check_quota('A','artisan_basic','documents_imported')
    assert not q['ok']
