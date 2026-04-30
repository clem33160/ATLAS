import os, subprocess
from atlas_governance.core.common import project_root
from atlas_governance.agents.worktree_guard import worktree_status
def whereami():
    rap=(project_root()/"atlas_rapporteur").exists()
    try: br=subprocess.check_output(['git','rev-parse','--abbrev-ref','HEAD'],text=True).strip()
    except Exception: br='unknown'
    return {"project_root":str(project_root()),"current_workdir":os.getcwd(),"governance_root":str(project_root()/"atlas_governance"),"active_manifest":"atlas_governance/config/atlas_manifest_core.json","active_authority_index":"atlas_governance/config/atlas_authority_index.json","active_domain_registry":"atlas_governance/config/atlas_domain_registry.json","rapporteur_detected":rap,"active_rapporteur_path":"atlas_rapporteur" if rap else None,"current_git_branch":br,"dirty_files_count":worktree_status()['dirty_files_count'],"health_status":"OK"}
