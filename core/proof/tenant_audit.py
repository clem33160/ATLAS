import hashlib
EVENT_TYPES={"tenant_created","user_invited","connector_linked","document_imported","document_classified","document_delivered","access_denied","hash_changed_refusal","export_requested","deletion_requested","backup_created","restore_tested"}
class TenantAuditChain:
    def __init__(self): self.events=[]
    def append(self, tenant_id:str, event_type:str, payload:dict):
        if event_type not in EVENT_TYPES: raise ValueError("invalid event type")
        tenant_events=[x for x in self.events if x['tenant_id']==tenant_id]
        prev=tenant_events[-1]['hash'] if tenant_events else 'GENESIS'
        raw=f"{tenant_id}|{event_type}|{payload}|{prev}".encode()
        h=hashlib.sha256(raw).hexdigest()
        e={"tenant_id":tenant_id,"event_type":event_type,"payload":payload,"prev":prev,"hash":h}
        self.events.append(e); return e
    def verify_tenant(self, tenant_id:str)->bool:
        prev="GENESIS"
        for e in [x for x in self.events if x['tenant_id']==tenant_id]:
            chk=hashlib.sha256(f"{tenant_id}|{e['event_type']}|{e['payload']}|{prev}".encode()).hexdigest()
            if chk!=e['hash']: return False
            prev=e['hash']
        return True
    def query(self, requester_role:str, requester_tenant_id:str, tenant_id:str):
        if requester_role!="platform_admin" and requester_tenant_id!=tenant_id: raise PermissionError("cross-tenant audit query refused")
        return [e for e in self.events if e['tenant_id']==tenant_id]
