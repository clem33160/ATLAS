def build_lead_report(leads_count: int, ready_count: int, warnings: list[str]) -> str:
    lines = [
        "# Atlas Rapporteur d’Affaires — Rapport V0.10",
        "",
        f"Leads totaux: {leads_count}",
        f"Leads BUSINESS_READY: {ready_count}",
        "",
        "## Avertissements gouvernance",
    ]
    lines += [f"- {w}" for w in warnings] if warnings else ["- Aucun avertissement critique."]
    return "\n".join(lines)
