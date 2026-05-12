from core.observability.metrics import MetricsStore
from core.observability.health import health_status

def test_metrics_health():
    m=MetricsStore(); m.inc('A','delivery_count'); assert m.get('A')['delivery_count']==1
    assert health_status()['status']=='ok'
