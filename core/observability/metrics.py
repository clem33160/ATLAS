class MetricsStore:
    def __init__(self): self.m={}
    def inc(self, tenant_id:str, metric:str, by:int=1): self.m.setdefault(tenant_id,{}).setdefault(metric,0); self.m[tenant_id][metric]+=by
    def get(self, tenant_id:str): return self.m.get(tenant_id,{})
