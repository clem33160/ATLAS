from __future__ import annotations

def resolve_memory_need(query_or_task:str)->dict:
    q=query_or_task.lower()
    mapping=[('améliorer rapporteur affaires',['objectives','active','procedures','canon','audit']),('preuve lead',['evidence','uncertainty','canon','audit']),('conflit',['conflict','uncertainty','canon','audit']),('que sais-tu',['raw','semantic','canon','index']),('pourquoi',['causal','audit','evidence']),('où aller maintenant',['objectives','active','anti_forgetting']),('nettoyer bruit',['noise_guard','noise_quarantine','health'])]
    layers=['raw','semantic']
    for k,v in mapping:
        if k in q: layers=v
    return {'query':query_or_task,'layers':layers,'files_consulted':[f'atlas_memory/src/{x}.py' for x in layers if x not in {'evidence','index','health','anti_forgetting'}],'reasons':'keyword mapping','risks':['incomplete query intent'],'confidence':0.72}
