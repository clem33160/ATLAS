from .common import repo_root

MAP = {
    "business_leads": "atlas/business",
    "governance_manifest": "atlas_governance/config/atlas_manifest_core.json",
    "governance_authority_index": "atlas_governance/config/atlas_authority_index.json",
    "governance_domain_registry": "atlas_governance/config/atlas_domain_registry.json",
    "atlas_manifest": "atlas_governance/config/atlas_manifest_core.json",
}

def resolve(key: str):
    rel = MAP.get(key)
    if not rel:
        return None
    return str(repo_root() / rel)
