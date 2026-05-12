import subprocess

from core.cli_reports import readiness_report


def test_cli_global_scale_contains_no_false_production_claim():
    out = subprocess.check_output(["bash", "scripts/atlas", "global-scale", "--entities", "2000000000"], text=True)
    assert "Production-ready for 2B entities: NO" in out


def test_readiness_mentions_health_not_ready():
    out = readiness_report()
    assert "Atlas Health production-ready: NO" in out


def test_readiness_mentions_public_saas_not_ready():
    out = readiness_report()
    assert "Public SaaS-ready: NO" in out
