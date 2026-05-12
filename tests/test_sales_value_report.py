from core.sales.value_report import build_value_report

def test_value_report():
    r=build_value_report({'time_saved':20,'risk_reduced':10})
    assert r['pilot_justified'] in {800,1000,1200,0}
