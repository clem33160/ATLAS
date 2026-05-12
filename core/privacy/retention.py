from dataclasses import dataclass
@dataclass
class RetentionPolicy:
    tenant_id:str
    retention_days:int
