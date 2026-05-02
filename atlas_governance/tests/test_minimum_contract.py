from pathlib import Path
import subprocess
from atlas_governance.core.root_anchor import find_root
from atlas_governance.core.constitution import validate_constitution
from atlas_governance.core.forbidden_name_guard import detect_forbidden_names
from atlas_governance.core.duplicate_detector import run_duplicate_detection
from atlas_governance.core.common import read_json, write_json
from atlas_governance.core.invariant_engine import run_invariants
from atlas_governance.core.path_resolver import resolve
from atlas_governance.recovery import lost_mode

ACTIVE_FILES = [
    'atlas_governance/core/common.py','atlas_governance/core/root_anchor.py','atlas_governance/core/constitution.py','atlas_governance/core/invariant_engine.py','atlas_governance/core/identity_fingerprint.py','atlas_governance/core/path_resolver.py','atlas_governance/core/system_map.py','atlas_governance/core/forbidden_name_guard.py','atlas_governance/core/duplicate_detector.py','atlas_governance/recovery/lost_mode.py','atlas_governance/recovery/boot_contract.py','atlas_governance/recovery/self_reconstruction_engine.py'
]

def test_import_package():
    import atlas_governance
    assert atlas_governance is not None

def test_root_anchor_from_subdir():
    root=find_root(Path('atlas_governance/tests'))
    assert (root/'.git').exists()

def test_constitution_has_12_laws():
    v=validate_constitution()
    assert v['ok'] and v['count']>=12

def test_invariants_vital_pieces_ok():
    r=run_invariants()
    assert r['ok']

def test_path_resolver_known_authorities():
    assert resolve('rapporteur_main')
    assert resolve('governance_manifest')

def test_forbidden_detection_on_authority_index():
    p=Path('atlas_governance/config/atlas_authority_index.json')
    data=read_json(p,{})
    orig=dict(data)
    data['tmp_test']='atlas_governance/final_tmp.py'
    write_json(p,data)
    try:
        found=detect_forbidden_names()
        assert any(tok in " ".join(found).lower() for tok in ['final','tmp'])
    finally:
        write_json(p,orig)

def test_duplicate_detector_runs():
    out=run_duplicate_detection()
    assert 'count' in out

def test_lost_mode_toggle():
    lost_mode.activate_lost_mode(); assert lost_mode.is_lost_mode_active(); assert not lost_mode.safe_to_modify()
    lost_mode.deactivate_lost_mode(); assert not lost_mode.is_lost_mode_active()

def test_dashboard_generation_and_score_drop_check():
    subprocess.check_call(['bash','atlas_governance/scripts/atlas_imperdability_dashboard.sh'])
    j=Path('atlas_governance/runtime/dashboard/imperdability_dashboard.json')
    m=Path('atlas_governance/runtime/dashboard/imperdability_dashboard.md')
    assert j.exists() and m.exists()
    data=read_json(j,{})
    assert data['imperdability_score'] >= 85


def test_no_active_module_decorative_stub():
    for fp in ACTIVE_FILES:
        txt=Path(fp).read_text(encoding='utf-8')
        assert 'return {"ok": True}' not in txt
        assert 'def run(*args, **kwargs):\n    return' not in txt

def test_runtime_only_gitkeep_tracked():
    out=subprocess.check_output(['git','ls-files','atlas_governance/runtime'], text=True).strip().splitlines()
    assert out == ['atlas_governance/runtime/.gitkeep']
