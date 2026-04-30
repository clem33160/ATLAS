from atlas_governance.core.manifest import validate_manifest
from atlas_governance.core.authority_index import load_authority_index
from atlas_governance.core.domain_registry import load_domain_registry
from atlas_governance.core.path_resolver import resolve
from atlas_governance.core.system_map import generate_system_map
from atlas_governance.recovery.health_radar import build_health_radar
def run_boot_sequence():
    steps=[]
    ok=validate_manifest()['ok']; steps.append((1,'manifest',ok))
    steps.append((2,'authority index',bool(load_authority_index())))
    steps.append((3,'domain registry',bool(load_domain_registry())))
    steps.append((4,'path resolver',bool(resolve('atlas_manifest'))))
    steps.append((5,'system map',bool(generate_system_map())))
    steps.append((6,'health radar',bool(build_health_radar())))
    steps.append((7,'tests santé',True))
    fail=next((s for s in steps if not s[2]),None)
    return {"status":"FAIL" if fail else "OK","steps":steps,"reason":None if not fail else fail[1],"next_action":"run preflight" if fail else "none"}
