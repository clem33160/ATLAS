from atlas_governance.core.common import repo_root, write_json, write_md
from atlas_governance.recovery.lost_mode import is_lost_mode_active

def run():
    r=repo_root()
    req={
      "manifest": r/"atlas_governance/config/atlas_manifest_core.json",
      "constitution": r/"atlas_governance/config/atlas_constitution_core.json",
      "authority_index": r/"atlas_governance/config/atlas_authority_index.json",
      "domain_registry": r/"atlas_governance/config/atlas_domain_registry.json",
      "path_resolver": r/"atlas_governance/core/path_resolver.py",
      "invariant_engine": r/"atlas_governance/core/invariant_engine.py",
      "audit_ledger": r/"atlas_governance/audit/append_only_ledger.py",
      "runtime": r/"atlas_governance/runtime",
    }
    checks={k:v.exists() for k,v in req.items()}
    checks["lost_mode_inactive"]=not is_lost_mode_active()
    ok=all(checks.values())
    out={"ok":ok,"checks":checks}
    write_json(r/"atlas_governance/runtime/reports/boot_contract.json",out)
    write_md(r/"atlas_governance/runtime/reports/boot_contract.md","# Boot Contract\n"+"\n".join(f"- {k}: {'OK' if v else 'FAIL'}" for k,v in checks.items()))
    return out
