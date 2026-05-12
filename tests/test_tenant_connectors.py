from core.connectors.oauth_state import build_oauth_state
from core.connectors.tenant_connector_registry import TenantConnectorRegistry

def test_connector_registry_and_oauth_state():
    s=build_oauth_state('A'); assert s['tenant_id']=='A' and s['nonce']
    r=TenantConnectorRegistry(); r.link('A','google_drive','~/atlas_data/tokens/A.json'); assert 'google_drive' in r.data['A']
