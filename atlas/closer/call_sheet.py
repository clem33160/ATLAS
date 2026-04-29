from atlas.models import QUALIFICATION_BUSINESS_READY, REALITY_DEMO


def build_daily_call_sheet(leads: list[dict], artisans: list[dict]) -> tuple[str, list[dict]]:
    ready = [l for l in leads if l.get("qualification_status") == QUALIFICATION_BUSINESS_READY and l.get("reality_status") != REALITY_DEMO]
    validate = [l for l in leads if l not in ready and l.get("reality_status") != REALITY_DEMO]
    demos = [l for l in leads if l.get("reality_status") == REALITY_DEMO]
    rejected = [l for l in leads if l.get("pipeline_status") == "REJECTED"]
    lines = ["# Daily Call Sheet V0.10", "", "## À appeler maintenant (BUSINESS_READY)"]
    lines += [f"- {l['lead_id']} | {l.get('city','')} | {l.get('trade','')}" for l in ready] or ["- Aucun lead prêt."]
    lines += ["", "## À valider"] + [f"- {l['lead_id']}" for l in validate]
    lines += ["", "## Démo (ne pas appeler)"] + [f"- {l['lead_id']}" for l in demos]
    lines += ["", "## Rejetés"] + [f"- {l['lead_id']}" for l in rejected or [{"lead_id":"Aucun"}]]
    csv_rows = [{"segment": "business_ready", "lead_id": l["lead_id"]} for l in ready]
    csv_rows += [{"segment": "to_validate", "lead_id": l["lead_id"]} for l in validate]
    csv_rows += [{"segment": "demo", "lead_id": l["lead_id"]} for l in demos]
    return "\n".join(lines), csv_rows
