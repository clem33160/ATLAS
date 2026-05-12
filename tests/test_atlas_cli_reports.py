from core.cli_reports import readiness_report, value_report


def test_readiness_report_contains_scores_and_honesty():
    out = readiness_report()
    assert "Config:" in out
    assert "Proof1000:" in out
    assert "Pilot-ready: YES" in out
    assert "Public SaaS-ready: NO" in out
    assert "Blockers:" in out


def test_value_report_contains_pricing_and_non_saas_claim():
    out = value_report()
    assert "Documents processed:" in out
    assert "Estimated monthly value range:" in out
    assert "Pilot pricing 800 EUR justified:" in out
    assert "Pilot pricing 1000 EUR justified:" in out
    assert "Pilot pricing 1200 EUR justified:" in out
    assert "Production SaaS readiness claim: NO" in out
