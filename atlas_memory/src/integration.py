from __future__ import annotations
from pathlib import Path
from .raw_store import append_event
from .common import read_json

def create_system_event(kind,domain,content,confidence):
    return append_event({'kind':kind,'domain':domain,'content':content,'source':'system','confidence':confidence})

def ingest_rapporteur_run(summary_path=None,rejected_path=None,leads_path=None):
    res={}
    for k,p in {'summary':summary_path or 'atlas_rapporteur/runtime/reports/daily_report.json','rejected':rejected_path or 'atlas_rapporteur/runtime/audit/rejected_results.json','leads':leads_path or 'atlas_rapporteur/runtime/exports/leads_ranked.json'}.items():
      pp=Path(p)
      if pp.exists():
        payload=read_json(pp,{})
        create_system_event('rapporteur_ingest','rapporteur_affaires',f'{k} ingested',{ 'summary':0.9,'rejected':0.8,'leads':0.85}[k])
        res[k]='ingested'
      else:
        res[k]='missing'
    return res

def ingest_governance_health():
    return create_system_event('governance_health','governance','health check ingested',0.7)

def ingest_test_result(module,passed,warnings=0):
    return create_system_event('test_result',module,f'passed={passed} warnings={warnings}',0.8 if passed else 0.4)
