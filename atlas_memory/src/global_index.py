from __future__ import annotations
from .common import RUNTIME_PATHS, read_jsonl, write_json, now_iso
from . import canon_store, conflict_store, uncertainty_store, objective_store, procedure_store, simulation_store, health

def generate_global_index() -> dict:
    rep = health.compute_health()
    data = {
        'layers_status': {str(i): 'present' for i in range(1, 21)},
        'storage': {k: str(v) for k, v in RUNTIME_PATHS.items()},
        'canon_domains': canon_store.list_canon_domains(),
        'conflicts': len(conflict_store.list_conflicts()),
        'uncertainties': len(uncertainty_store.list_uncertainties()),
        'audit_count': len(read_jsonl(RUNTIME_PATHS['audit'])),
        'objective_count': len(objective_store.list_objectives()),
        'procedure_count': len(procedure_store.list_procedures()),
        'simulation_count': len(simulation_store.list_scenarios()),
        'memory_score': rep['memory_score'],
        'anti_noise_status': 'enabled',
        'governance_status': 'enabled',
        'last_generated_at': now_iso(),
    }
    write_json(RUNTIME_PATHS['index'], data)
    md = RUNTIME_PATHS['index'].with_suffix('.md')
    md.write_text('\n'.join(['# Global Memory Map'] + [f'- {k}: {v}' for k, v in data.items()]), encoding='utf-8')
    return data
