from core.billing.plans import PLANS
METRICS=["documents_imported","documents_indexed","searches","deliveries","connector_syncs","OCR_pages","users","storage_mb","audit_events"]
class UsageLedger:
    def __init__(self): self.usage={}
    def add(self, tenant_id:str, metric:str, value:int=1): self.usage.setdefault(tenant_id,{}).setdefault(metric,0); self.usage[tenant_id][metric]+=value
    def check_quota(self, tenant_id:str, plan:str, metric:str):
        limit=PLANS[plan].get(metric,10**9); used=self.usage.get(tenant_id,{}).get(metric,0)
        return {"used":used,"limit":limit,"ok":used<=limit,"warn":used>int(limit*0.9)}
