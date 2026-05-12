from core.data_sources.registry import build_registry

def test_sources_registry():
    row={'source_id':'x','source_type':'k','local_path':'p','enabled':True,'sensitivity':'low','allowed_roles':['owner'],'provenance_rules':{},'test_status':'ok'}
    r=build_registry([row])
    assert r[0].source_id=='x'
