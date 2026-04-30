from atlas_governance.core.manifest import validate_manifest
from atlas_governance.core.authority_index import detect_missing_authorities
from atlas_governance.core.system_map import generate_system_map
from atlas_governance.core.forbidden_name_guard import detect_forbidden_names
from atlas_governance.core.duplicate_detector import run_duplicate_detection
from atlas_governance.core.single_authority_gate import validate_single_authority
from atlas_governance.core.common import runtime_dir, write_json, write_md
def run_preflight():
    report={"manifest":validate_manifest(),"missing_authorities":detect_missing_authorities(),"system_map":generate_system_map(),"forbidden":detect_forbidden_names(),"duplicates":run_duplicate_detection(),"single_authority":validate_single_authority()}
    write_json(runtime_dir()/"reports/preflight_report.json",report); write_md(runtime_dir()/"reports/preflight_report.md",str(report)); return report
