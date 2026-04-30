from .authority_index import load_authority_index
from .common import runtime_dir, write_json

def detect_authority_conflicts():
    seen={}; conflicts=[]
    for k,v in load_authority_index().items():
        if v in seen: conflicts.append({"roles":[seen[v],k],"path":v})
        seen[v]=k
    return conflicts
def validate_single_authority():
    c=detect_authority_conflicts(); return {"ok":len(c)==0,"conflicts":c}
def write_authority_conflict_report():
    out=validate_single_authority(); write_json(runtime_dir()/"reports/authority_conflicts.json",out); return out
