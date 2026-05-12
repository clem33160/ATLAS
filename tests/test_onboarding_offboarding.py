from core.onboarding.checklist import onboarding_checklist
from core.offboarding.export import export_tenant_data
from core.offboarding.delete_request import create_delete_request

def test_onboard_offboard_contracts():
    assert 'tenant created' in onboarding_checklist()
    assert export_tenant_data('A')['status']=='exported'
    assert create_delete_request('A')['destructive'] is False
