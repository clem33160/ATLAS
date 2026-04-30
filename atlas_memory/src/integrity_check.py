from __future__ import annotations
from .global_index import generate_global_index
from .anti_forgetting import run_anti_forgetting_check

def run_integrity_check()->dict:
    idx=generate_global_index()
    af=run_anti_forgetting_check()
    return {'global_index_ok':bool(idx),'anti_forgetting_ok':all(af.values())}
