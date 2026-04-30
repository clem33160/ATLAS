import json
from pathlib import Path

from atlas_rapporteur.src.main import run
from atlas_rapporteur.src.models import Lead
from atlas_rapporteur.src.compliance import is_potential_lead


def test_budget_stop_avant_requete(monkeypatch):
    monkeypatch.setenv("GOOGLE_CSE_API_KEY", "k")
    monkeypatch.setenv("GOOGLE_CSE_CX", "cx")
    leads, summary = run("google-cse", limit=20, with_summary=True)
    assert "stopped_by_budget" in summary


def test_anti_annuaire():
    l = Lead(title="Annuaire plombier", url="https://x", snippet="annuaire lyon", city="Lyon", trade="plombier")
    assert not is_potential_lead(l)


def test_anti_blog():
    l = Lead(title="Blog rénovation", url="https://x", snippet="blog sur travaux", city="Lyon", trade="rénovation")
    assert not is_potential_lead(l)


def test_anti_emploi():
    l = Lead(title="Offre emploi plombier", url="https://x", snippet="emploi", city="Lyon", trade="plombier")
    assert not is_potential_lead(l)


def test_anti_formation():
    l = Lead(title="Formation chauffagiste", url="https://x", snippet="formation", city="Lyon", trade="chauffagiste")
    assert not is_potential_lead(l)


def test_page_client_reelle_acceptee():
    l = Lead(title="Besoin devis plomberie", url="https://x", snippet="cherche plombier fuite urgent lyon", city="Lyon", trade="plombier")
    assert is_potential_lead(l)


def test_pdf_illisible_rejete():
    l = Lead(title="Demande", url="https://x/doc.pdf", snippet="pdf", city="Lyon", trade="plombier")
    assert not is_potential_lead(l)


def test_exports_presents():
    run("dry-run", limit=5)
    base = Path("atlas_rapporteur/runtime")
    assert (base / "exports/leads_ranked.csv").exists()
    assert (base / "exports/leads_ranked.json").exists()
    assert (base / "reports/daily_report.md").exists()


def test_aucun_business_ready_sans_validation_humaine():
    leads = run("dry-run", limit=5)
    assert all(l.tier != "BUSINESS_READY" for l in leads)
    data = json.loads(Path("atlas_rapporteur/runtime/exports/leads_ranked.json").read_text(encoding="utf-8"))
    assert all(d["tier"] != "BUSINESS_READY" for d in data)
