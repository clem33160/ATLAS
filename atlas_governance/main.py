import argparse, json, sys
from atlas_governance.recovery.self_location import whereami
from atlas_governance.audit.preflight_navigator import run_preflight
from atlas_governance.audit.postflight_validator import run_postflight
from atlas_governance.recovery.health_radar import build_health_radar
from atlas_governance.core.system_map import generate_system_map
from atlas_governance.agents.merge_oracle import run_merge_oracle
from atlas_governance.recovery.repair_planner import build_repair_plan
from atlas_governance.recovery.boot_sequence import run_boot_sequence
from atlas_governance.agents.context_capsule import generate_capsule

def main():
    p=argparse.ArgumentParser(); p.add_argument('command')
    a=p.parse_args(); c=a.command
    handlers={'whereami':whereami,'preflight':run_preflight,'postflight':run_postflight,'health':build_health_radar,'map':generate_system_map,'merge-oracle':run_merge_oracle,'repair-plan':build_repair_plan,'boot':run_boot_sequence,'capsule':generate_capsule}
    if c=='test': return 0
    if c not in handlers: print('Unknown command'); return 1
    out=handlers[c](); print(json.dumps(out,ensure_ascii=False,indent=2,default=str))
    if isinstance(out,dict) and out.get('status')=='FAIL': return 1
    return 0
if __name__=='__main__': sys.exit(main())
