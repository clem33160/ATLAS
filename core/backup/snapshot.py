import hashlib

def build_snapshot_manifest(tenant_id:str, entries:list[str]):
    checksum=hashlib.sha256("|".join(sorted(entries)).encode()).hexdigest()
    return {"tenant_id":tenant_id,"entries":entries,"checksum":checksum}
