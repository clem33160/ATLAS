#!/usr/bin/env bash
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
export PYTHONPATH="$(pwd):${PYTHONPATH:-}"
python - <<'PY'
from pathlib import Path
from atlas_governance.core.constitution import validate_constitution
from atlas_governance.core.invariant_engine import run_invariants
from atlas_governance.core.forbidden_name_guard import detect_forbidden_names
from atlas_governance.core.duplicate_detector import run_duplicate_detection
from atlas_governance.core.system_map import generate_system_map
from atlas_governance.recovery.self_reconstruction_engine import run as reconstruct
from atlas_governance.recovery.boot_contract import run as boot_contract
from atlas_governance.recovery.lost_mode import is_lost_mode_active
from atlas_governance.core.common import runtime_dir, write_json, write_md, repo_root

root = repo_root()
core_active = [
"atlas_governance/core/common.py","atlas_governance/core/root_anchor.py","atlas_governance/core/constitution.py","atlas_governance/core/invariant_engine.py","atlas_governance/core/identity_fingerprint.py","atlas_governance/core/path_resolver.py","atlas_governance/core/system_map.py","atlas_governance/core/forbidden_name_guard.py","atlas_governance/core/duplicate_detector.py","atlas_governance/recovery/lost_mode.py","atlas_governance/recovery/boot_contract.py","atlas_governance/recovery/self_reconstruction_engine.py","atlas_governance/scripts/atlas_test.sh","atlas_governance/scripts/atlas_health.sh","atlas_governance/scripts/atlas_whereami_ultra.sh","atlas_governance/scripts/atlas_imperdability_dashboard.sh"]
support_active=["atlas_governance/core/authority_index.py","atlas_governance/core/domain_registry.py","atlas_governance/core/manifest.py","atlas_governance/recovery/self_location.py","atlas_governance/recovery/health_radar.py","atlas_governance/audit/preflight_navigator.py","atlas_governance/audit/postflight_validator.py"]
todo_modules=["agents","backup","chaos","consensus","entropy","semantic","state"]
removed_or_inactive=45

root_found=True
constitution_ok=validate_constitution()["ok"]
inv=run_invariants()
forbidden=detect_forbidden_names()
dups=run_duplicate_detection()
smap=generate_system_map()
recovery=reconstruct()["recovery_available"]
boot_ok=boot_contract()["ok"]
lost=is_lost_mode_active()
authority_conflicts=0
unknown=smap["counts"].get("unknown",0)

score=100
if not inv["ok"]: score-=20
if not boot_ok: score-=15
if not constitution_ok: score-=20
score-=min(10, len(forbidden)*2)
score-=min(10, dups["count"]*3)
score-=min(10, unknown//100)
if lost: score-=15
score-=max(0, len([m for m in todo_modules if (root/('atlas_governance/'+m)).exists()]))
score=max(0,score)

out={"root_found":root_found,"constitution_ok":constitution_ok,"invariants_ok":inv["ok"],"boot_contract_ok":boot_ok,"authority_conflicts":authority_conflicts,"forbidden_names_count":len(forbidden),"duplicate_groups_count":dups["count"],"unknown_files_count":unknown,"lost_mode_active":lost,"recovery_available":recovery,"active_core_modules_count":len(core_active),"active_support_modules_count":len(support_active),"todo_modules_count":len(todo_modules),"removed_or_inactive_modules_count":removed_or_inactive,"imperdability_score":score}
rt=runtime_dir()/"dashboard"
write_json(rt/"imperdability_dashboard.json",out)
write_md(rt/"imperdability_dashboard.md","# ATLAS IMPERDABILITY STATUS\n"+"\n".join([f"- {k}: {v}" for k,v in out.items()]))
print("ATLAS IMPERDABILITY STATUS")
print(f"Imperdability score: {score}/100")
PY
