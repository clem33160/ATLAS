import json
from pathlib import Path
from atlas_rapporteur.src.models import Lead
from atlas_rapporteur.src.reports import write_exports


def test_reports_stricts():
    l1 = Lead(title="Besoin plomberie Lyon", source_url="https://x/1", city="Lyon", country="FR", trade="plomberie", evidence_summary="preuve", raw_snippet="preuve", qualification_status="TO_VALIDATE", score=70, tier="GROS")
    l2 = Lead(title="Ready", source_url="https://x/2", city="Lyon", country="FR", trade="plomberie", evidence_summary="preuve", raw_snippet="preuve", qualification_status="BUSINESS_READY", score=90, tier="TITAN")
    rejected = [{"title": "bad", "reason": "REJECTED_INVALID_URL"}]
    write_exports([l1, l2], rejected=rejected, query_costs=[{"estimated_cost_eur": 0.005}], summary={"results_retrieved": 3, "queries_used": 2, "estimated_cost_eur": 0.01, "budget_remaining_queries": 98})

    base = Path("atlas_rapporteur/runtime")
    csv_text = (base / "exports/leads_ranked.csv").read_text(encoding="utf-8")
    assert "Besoin plomberie Lyon" in csv_text and "Ready" not in csv_text

    closer = (base / "closer/closer_call_sheet.md").read_text(encoding="utf-8")
    assert "## À appeler maintenant" in closer and "Ready" in closer
    assert "Besoin plomberie Lyon | Lyon | plomberie" in closer

    rej = json.loads((base / "audit/rejected_results.json").read_text(encoding="utf-8"))
    assert rej and rej[0]["reason"] == "REJECTED_INVALID_URL"


def test_no_business_ready_without_human_validation():
    lead = Lead(title="A", source_url="https://x", city="Lyon", country="FR", trade="plomberie", evidence_summary="x", raw_snippet="x")
    assert lead.qualification_status == "TO_VALIDATE"
