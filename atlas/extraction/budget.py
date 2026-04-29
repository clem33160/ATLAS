from __future__ import annotations
import re

def detect_budget(text:str)->dict:
    t=(text or '').lower()
    vals=[int(x) for x in re.findall(r'(\d{2,7})\s*€', t)]
    if not vals:
        return {'budget_low':0,'budget_mid':0,'budget_high':0,'budget_status':'ESTIMATED'}
    v=vals[0]
    return {'budget_low':int(v*0.8),'budget_mid':v,'budget_high':int(v*1.2),'budget_status':'VISIBLE'}
