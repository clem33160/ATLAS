from pathlib import Path
from .common import read_json, project_root

def load_manifest(): return read_json(project_root()/"atlas_governance/config/atlas_manifest_core.json", {})
def validate_manifest():
    m=load_manifest(); req=["system_name","governance_name","logical_version","root_markers"]
    missing=[k for k in req if k not in m]
    return {"ok":not missing,"missing":missing}
def get_project_root()->Path: return project_root()
def explain_manifest():
    m=load_manifest(); v=validate_manifest();
    return {"manifest":m,"validation":v,"project_root":str(project_root())}
