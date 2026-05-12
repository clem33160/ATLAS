class RateLimiter:
    def __init__(self): self._counts = {}
    def hit(self, tenant_id: str, key: str, limit: int) -> bool:
        ckey=(tenant_id,key); self._counts[ckey]=self._counts.get(ckey,0)+1
        return self._counts[ckey] <= limit
