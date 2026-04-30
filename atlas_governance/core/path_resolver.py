from .authority_index import get_authority
from .domain_registry import get_domain
from .common import project_root, suspicious_name

def resolve(role_or_domain):
    auth=get_authority(role_or_domain)
    if auth: return str(project_root()/auth)
    d=get_domain(role_or_domain)
    if d: return d.get("allowed_directories",[])[0]
    return None
def explain_resolution(role_or_domain): return {"input":role_or_domain,"resolved":resolve(role_or_domain)}
def is_canonical_path(path): return not suspicious_name(str(path))
def is_allowed_for_domain(path, domain_id):
    d=get_domain(domain_id) or {}
    p=str(path)
    return any(seg in p for seg in d.get("allowed_directories",[])) and not any(seg in p for seg in d.get("forbidden_directories",[]))
def reject_ambiguous_path(path): return not suspicious_name(str(path))
def detect_path_confusion(path): return {"path":str(path),"confused":suspicious_name(str(path))}
