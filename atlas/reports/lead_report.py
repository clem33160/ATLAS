def build_lead_report(leads_count: int, ready_count: int, warnings: list[str], leads: list[dict], human_warnings: list[str]) -> str:
    lines = [
        "# Atlas Rapporteur d’Affaires — Rapport V0.10",
        "",
        f"Leads totaux: {leads_count}",
        f"Leads BUSINESS_READY: {ready_count}",
        "",
        "## Avertissements gouvernance",
    ]
    lines += [f"- {w}" for w in warnings] if warnings else ["- Aucun avertissement critique."]
    lines += ["", "## Validation humaine"]
    for lead in leads:
        if lead.get("human_validation_status"):
            lines.append(f"- {lead.get('lead_id')}: {lead.get('human_validation_status')} ({lead.get('human_validation_reason','')})")
    lines += [f"- warning: {w}" for w in human_warnings]
    return "\n".join(lines)
