import unittest, subprocess
from atlas_governance.core.manifest import load_manifest
from atlas_governance.core.authority_index import load_authority_index
from atlas_governance.core.domain_registry import load_domain_registry
from atlas_governance.core.path_resolver import resolve
from atlas_governance.core.forbidden_name_guard import detect_forbidden_names
from atlas_governance.core.duplicate_detector import run_duplicate_detection
from atlas_governance.core.single_authority_gate import validate_single_authority
from atlas_governance.core.system_map import generate_system_map
from atlas_governance.recovery.self_location import whereami
from atlas_governance.recovery.health_radar import build_health_radar
from atlas_governance.audit.preflight_navigator import run_preflight
from atlas_governance.audit.postflight_validator import run_postflight
from atlas_governance.agents.merge_oracle import run_merge_oracle
from atlas_governance.agents.task_scope_lock import validate_scope
from atlas_governance.graphs.evidence_resolver import validate_no_business_lead_without_source
from atlas_governance.recovery.boot_sequence import run_boot_sequence

class T(unittest.TestCase):
    def test_manifest_loads(self): self.assertIn('system_name', load_manifest())
    def test_authority_index_loads(self): self.assertTrue(load_authority_index())
    def test_domain_registry_loads(self): self.assertGreaterEqual(len(load_domain_registry()), 15)
    def test_path_resolver_finds_rapporteur(self): self.assertTrue(resolve('atlas_manifest'))
    def test_forbidden_name_detection(self): self.assertIsInstance(detect_forbidden_names(), list)
    def test_duplicate_detector_runs(self): self.assertIn('count', run_duplicate_detection())
    def test_single_authority_gate(self): self.assertIn('ok', validate_single_authority())
    def test_system_map_generated(self): self.assertIn('count', generate_system_map())
    def test_whereami_command(self): self.assertIn('project_root', whereami())
    def test_health_radar(self): self.assertIn('health_score', build_health_radar())
    def test_preflight_report(self): self.assertIn('manifest', run_preflight())
    def test_postflight_report(self): self.assertIn('postflight', run_postflight())
    def test_merge_oracle(self): self.assertIn('diff', run_merge_oracle())
    def test_no_runtime_generated_files_tracked(self):
        o=subprocess.check_output(['git','status','--porcelain','atlas_governance/runtime'], text=True)
        self.assertEqual(o.strip(), '')
    def test_agent_scope_lock(self): self.assertFalse(validate_scope({'task_type':'scoring'},['search/x.py'])['ok'])
    def test_evidence_resolver_no_fake_claims(self): self.assertTrue(validate_no_business_lead_without_source()['ok'])
    def test_boot_sequence(self): self.assertIn('status', run_boot_sequence())

if __name__=='__main__': unittest.main()
