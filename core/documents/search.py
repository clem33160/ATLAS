def search_docs(items: list[dict], query: str) -> dict:
    hits = [x for x in items if query.lower() in str(x).lower()]
    if len(hits) == 1: return {"status":"unique", "result": hits[0]}
    if len(hits) > 1: return {"status":"multiple", "choices": hits}
    return {"status":"none"}
