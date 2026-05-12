def search_by_doc_id(index, tenant_id: str, doc_id: str):
    if not tenant_id: raise ValueError("tenant_id required")
    scoped=f"{tenant_id}:{doc_id}"
    if scoped in index.docs: return {"status":"unique","doc":index.docs[scoped]}
    return {"status":"not_found"}
