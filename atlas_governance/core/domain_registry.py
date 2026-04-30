from .common import read_json, project_root

def load_domain_registry(): return read_json(project_root()/"atlas_governance/config/atlas_domain_registry.json", {})
def get_domain(domain_id): return load_domain_registry().get(domain_id)
def list_domains(): return list(load_domain_registry().keys())
def validate_domain_coverage():
    d=load_domain_registry(); return {"count":len(d),"ok":len(d)>=15}
def assign_path_to_domain(path):
    p=str(path)
    if "governance" in p: return "governance"
    if "test" in p: return "tests"
    if "score" in p: return "scoring"
    if "report" in p: return "reports"
    return "navigation"
