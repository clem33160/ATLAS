def numbered_choices(rows: list[dict]) -> str:
    return "\n".join([f"{i+1}. {r['label']} | {r['amount']} EUR | {r['location']} | {r['date']} | {r['doc_id']}" for i,r in enumerate(rows)])
