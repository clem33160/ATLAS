import subprocess

from core.cli_reports import readiness_report


def test_cli_global_scale_contains_no_false_production_claim():
    out = subprocess.check_output(["bash", "scripts/atlas", "global-scale", "--entities", "2000000000"], text=True)
    assert "Production-ready for 2B entities: NO" in out


def test_cli_global_scale_persons_uses_health_model_section():
    out = subprocess.check_output(["bash", "scripts/atlas", "global-scale", "--persons", "15000000000"], text=True)
    assert "ATLAS GLOBAL PERSON/HEALTH SCALE MODEL" in out
    assert "Target persons: 15,000,000,000" in out
    assert "Atlas Health production-ready: NO" in out
    assert "Health architecture model ready: YES" in out


def test_cli_global_scale_with_entities_and_persons_prints_both_sections():
    out = subprocess.check_output(
        ["bash", "scripts/atlas", "global-scale", "--entities", "2000000000", "--persons", "15000000000"],
        text=True,
    )
    assert "ATLAS GLOBAL ENTITY SCALE MODEL" in out
    assert "ATLAS GLOBAL PERSON/HEALTH SCALE MODEL" in out


def test_readiness_mentions_health_not_ready():
    out = readiness_report()
    assert "Atlas Health production-ready: NO" in out


def test_readiness_mentions_public_saas_not_ready():
    out = readiness_report()
    assert "Public SaaS-ready: NO" in out
