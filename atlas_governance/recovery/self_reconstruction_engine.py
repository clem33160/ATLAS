from atlas_governance.core.common import repo_root, write_json, write_md

def run():
    r=repo_root()
    candidates=["atlas_governance/config/atlas_manifest_core.json","atlas_governance/config/atlas_authority_index.json","atlas_governance/config/atlas_domain_registry.json","atlas_governance/config/atlas_constitution_core.json"]
    existing=[p for p in candidates if (r/p).exists()]
    data={"root":str(r),"existing_critical":existing,"recovery_available":len(existing)>=3}
    write_json(r/"atlas_governance/runtime/recovery/reconstructed_map.json",data)
    write_md(r/"atlas_governance/runtime/recovery/reconstructed_map.md","# Reconstructed Map\n"+"\n".join(f"- {x}" for x in existing))
    return data
