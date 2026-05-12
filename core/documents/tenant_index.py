class TenantDocumentIndex:
    def __init__(self): self.docs = {}
    def index(self, tenant_id: str, doc: dict):
        if not tenant_id: raise ValueError("tenant_id required")
        doc_id = doc["doc_id"]
        scoped = f"{tenant_id}:{doc_id}"
        payload = {**doc, "tenant_id": tenant_id, "scoped_doc_id": scoped}
        self.docs[scoped] = payload
        return payload
