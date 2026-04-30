from __future__ import annotations
from typing import Any
VALUES=['CRITICAL','IMPORTANT','USEFUL','SECONDARY','ANECDOTAL','DISCARDABLE']

def classify_value(item: dict[str, Any]) -> str:
    t=(str(item)).lower()
    if any(k in t for k in ['invariant','canon','governance','supreme']): return 'CRITICAL'
    if 'error' in t or 'conflict' in t: return 'IMPORTANT'
    if any(k in t for k in ['demo','test','mock','placeholder']): return 'DISCARDABLE'
    if any(k in t for k in ['report','summary','temporary']): return 'USEFUL'
    return 'SECONDARY'

def rank_by_value(items:list[dict[str,Any]])->list[dict[str,Any]]:
    order={v:i for i,v in enumerate(VALUES)}
    return sorted(items,key=lambda x:order.get(classify_value(x),99))

def explain_value(item: dict[str, Any]) -> dict[str, Any]:
    return {'value':classify_value(item),'item':item}
