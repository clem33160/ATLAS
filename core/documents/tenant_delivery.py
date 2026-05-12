import hashlib
from pathlib import Path

def deliver_tenant_doc(doc: dict, tenant_id: str, out_dir: Path):
    if tenant_id != doc.get("tenant_id"): raise PermissionError("cross-tenant access refused")
    p=Path(doc["path"])
    digest=hashlib.sha256(p.read_bytes()).hexdigest()
    if digest != doc.get("sha256"): raise PermissionError("hash-change refusal")
    out_dir.mkdir(parents=True, exist_ok=True)
    out=out_dir/f"{doc['scoped_doc_id'].replace(':','_')}.bin"
    out.write_bytes(p.read_bytes())
    return {"status":"ok","path":str(out)}
