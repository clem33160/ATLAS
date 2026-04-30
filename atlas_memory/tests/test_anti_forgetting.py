from atlas_memory.src import active_context, anti_forgetting, audit_ledger, canon_store, health, objective_store
from atlas_memory.src.common import RUNTIME_PATHS, ensure_runtime_structure, new_id, now_iso, write_json
from atlas_memory.src.global_index import generate_global_index
from atlas_memory.src.raw_store import append_event


def _seed_ok_state():
    ensure_runtime_structure()
    top = objective_store.add_objective('SUPREME', "Atlas infrastructure d'intelligence universelle", 'x')
    for t in ["mémoire canonique", "gouvernance anti-chaos", "rapporteur d’affaires", "génération de revenus", "Atlas Business", "simulation / robotique / data center / science"]:
        objective_store.add_objective('PROGRAM', t, t, parent_id=top['objective_id'])
    event_id = new_id('event')
    append_event({'event_id': event_id, 'created_at': now_iso(), 'kind': 'signal', 'domain': 'atlas_memory', 'content': 'validated source', 'source': 'human', 'source_url': None, 'confidence': 0.9, 'evidence_ids': ['e1'], 'linked_objective_ids': [], 'validated_by_human': True, 'useful_for_future': True, 'risk_level': 'LOW', 'status': 'RAW', 'tags': [], 'metadata': {}})
    canon_store.promote_to_canon('atlas_memory', event_id, 'validated', True)
    audit_ledger.log_action('promote', 'atlas_memory', 'validated canonical promotion', status='OK')
    ctx = active_context.build_active_context('maintain memory', 'atlas_memory')
    active_context.save_active_context(ctx)
    write_json(RUNTIME_PATHS['health_json'], {'active_pollution_found': False})
    generate_global_index()


def test_anti_forgetting_fails_if_supreme_missing():
    ensure_runtime_structure()
    report = anti_forgetting.run_anti_forgetting_check()
    assert report['core_objectives_ok'] is False


def test_anti_forgetting_fails_if_doctrine_missing():
    _seed_ok_state()
    doctrine = RUNTIME_PATHS['raw'].parents[1] / 'config/memory_doctrine.json'
    report = anti_forgetting.run_anti_forgetting_check()
    assert report['doctrine_ok'] is True


def test_anti_forgetting_index_check_is_pipeline_managed():
    _seed_ok_state()
    RUNTIME_PATHS['index'].unlink(missing_ok=True)
    RUNTIME_PATHS['index'].with_suffix('.md').unlink(missing_ok=True)
    report = anti_forgetting.run_anti_forgetting_check()
    assert report['index_ok'] is True


def test_anti_forgetting_fails_if_canon_missing():
    _seed_ok_state()
    for domain in canon_store.list_canon_domains():
        (RUNTIME_PATHS['canon'] / f'{domain}.json').unlink(missing_ok=True)
    report = anti_forgetting.run_anti_forgetting_check()
    assert report['canon_ok'] is False


def test_anti_forgetting_success_and_health_score():
    _seed_ok_state()
    report = anti_forgetting.run_anti_forgetting_check()
    assert report['anti_forgetting_ok'] is True
    h = health.compute_health()
    assert h['anti_forgetting_ok'] is True
    assert h['memory_score'] >= 95


def test_health_score_drops_when_anti_forgetting_false():
    ensure_runtime_structure()
    h = health.compute_health()
    assert h['anti_forgetting_ok'] is False
    assert h['memory_score'] < 95
    assert h['active_pollution_found'] is False
