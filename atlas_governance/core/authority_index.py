from .common import read_json, project_root

def load_authority_index(): return read_json(project_root()/"atlas_governance/config/atlas_authority_index.json", {})
def get_authority(domain_or_role): return load_authority_index().get(domain_or_role)
def list_authorities(): return load_authority_index()
def detect_missing_authorities():
    p=project_root(); return {k:v for k,v in load_authority_index().items() if not (p/v).exists()}
def detect_invalid_authority_paths(): return detect_missing_authorities()
def detect_multiple_authorities_for_same_domain(): return {}
