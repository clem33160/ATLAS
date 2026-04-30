from atlas_memory.src.memory_resolver import resolve_memory_need

def test_memory_resolver_key_queries():
    r=resolve_memory_need('conflit')
    assert 'conflict' in r['layers']
