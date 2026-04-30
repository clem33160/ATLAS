from atlas_memory.src.global_index import generate_global_index

def test_global_index_generation():
    r=generate_global_index()
    assert 'memory_score' in r
