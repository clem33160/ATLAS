import json
import subprocess
import unittest
from pathlib import Path

from atlas.business.readiness import compute_business_readiness
from atlas.governance import validate_no_fake_real_data
from atlas.main import apply_human_confirmations, run_pipeline
from atlas.models import QUALIFICATION_BUSINESS_READY, REALITY_DEMO


class PipelineTests(unittest.TestCase):
    def test_architecture_canonical(self):
        self.assertTrue(Path("atlas/main.py").exists())
        self.assertFalse(Path("atlas/rapporteur.py").exists())
        for required in ["config", "sources", "extraction", "artisans", "crm", "reports", "business", "closer", "runtime", "examples", "inbox", "scripts", "tests"]:
            self.assertTrue((Path("atlas") / required).exists())

    def test_runtime_only_outputs(self):
        run_pipeline()
        self.assertFalse(Path("atlas/export").exists())
        self.assertFalse(Path("atlas/leads").exists())
        self.assertFalse(Path("atlas/logs").exists())
        self.assertTrue(Path("atlas/runtime").exists())
        self.assertTrue(Path("atlas/runtime/reports/lead_report.md").exists())

    def test_no_fake_real(self):
        leads = [
            {"lead_id": "a", "source_url": "https://example.org/x", "qualification_status": QUALIFICATION_BUSINESS_READY, "reality_status": "COLLECTED_FROM_URL"},
            {"lead_id": "b", "source_url": "https://example.local/y", "qualification_status": "TO_VALIDATE", "reality_status": REALITY_DEMO},
        ]
        artisans = [{"name": "demo-art", "source_kind": REALITY_DEMO, "recommended_as_real": True}]
        errs = validate_no_fake_real_data(leads, artisans)
        self.assertTrue(any("Domaine fictif" in e for e in errs))
        self.assertTrue(any("Artisan DEMO" in e for e in errs))

    def test_business_score_honest(self):
        br = compute_business_readiness(leads=[], artisans=[])
        self.assertLessEqual(br["business_readiness_score"], 6)
        self.assertLessEqual(br["max_score_with_current_data"], 6)
        self.assertTrue(any("0 lead BUSINESS_READY" in x for x in br["blocking_reasons"]))
        self.assertTrue(any("0 artisan vérifiable" in x for x in br["blocking_reasons"]))

    def test_source_audit(self):
        completed = subprocess.run(["./atlas/scripts/source_audit.sh"], check=False, capture_output=True, text=True)
        self.assertEqual(completed.returncode, 0, msg=completed.stdout + completed.stderr)

    def test_runtime_outputs(self):
        run_pipeline()
        expected = [
            "atlas/runtime/reports/lead_report.md",
            "atlas/runtime/closer/daily_call_sheet.md",
            "atlas/runtime/closer/daily_call_sheet.csv",
            "atlas/runtime/business/business_readiness.md",
            "atlas/runtime/business/business_readiness.json",
            "atlas/runtime/export/leads_ranked.json",
        ]
        for out in expected:
            self.assertTrue(Path(out).exists(), msg=out)

    def test_scripts(self):
        commands = ["./atlas/scripts/run.sh", "./atlas/scripts/run.sh business", "./atlas/scripts/run.sh closer", "./atlas/scripts/run.sh crm-summary", "./atlas/scripts/run.sh verbose"]
        for cmd in commands:
            proc = subprocess.run(cmd, shell=True, check=False, capture_output=True, text=True)
            self.assertEqual(proc.returncode, 0, msg=f"{cmd}\n{proc.stdout}\n{proc.stderr}")
        proc = subprocess.run("./atlas/scripts/business_check.sh", shell=True, check=False, capture_output=True, text=True, env={"ATLAS_SKIP_TEST_SH": "1"})
        self.assertEqual(proc.returncode, 0, msg=f"./atlas/scripts/business_check.sh\n{proc.stdout}\n{proc.stderr}")

    def test_human_confirmation_valid_to_business_ready(self):
        leads = [{"lead_id": "l1", "source_url": "https://real.tld/1", "reality_status": "PARTIALLY_VERIFIED", "qualification_status": "TO_VALIDATE", "pipeline_status": "NEW"}]
        artisans = [{"source_kind": "OFFICIAL", "source_url": "https://artisan.tld"}]
        warnings = apply_human_confirmations(leads, artisans, [{
            "lead_id": "l1", "decision": "CONFIRM_BUSINESS_READY", "evidence_checked": "yes", "artisan_checked": "yes", "consent_status": "NON_DEMANDÉ"
        }])
        self.assertEqual(warnings, [])
        self.assertEqual(leads[0]["qualification_status"], "BUSINESS_READY")
        self.assertEqual(leads[0]["reality_status"], "HUMAN_CONFIRMED")
        self.assertEqual(leads[0]["pipeline_status"], "À_APPELER")

    def test_human_confirmation_demo_refused(self):
        leads = [{"lead_id": "l1", "source_url": "https://real.tld/1", "reality_status": "DEMO", "qualification_status": "TO_VALIDATE"}]
        artisans = [{"source_kind": "OFFICIAL", "source_url": "https://artisan.tld"}]
        apply_human_confirmations(leads, artisans, [{"lead_id": "l1", "decision": "CONFIRM_BUSINESS_READY", "evidence_checked": "yes", "artisan_checked": "yes", "consent_status": "NON_DEMANDÉ"}])
        self.assertEqual(leads[0]["qualification_status"], "TO_VALIDATE")
        self.assertIn("lead DEMO", leads[0]["human_validation_reason"])

    def test_human_confirmation_refusals_and_unknown(self):
        leads = [{"lead_id": "l1", "source_url": "https://real.tld/1", "reality_status": "PARTIALLY_VERIFIED", "qualification_status": "TO_VALIDATE"}]
        artisans = [{"source_kind": "DEMO", "source_url": "https://example.org"}]
        apply_human_confirmations(leads, artisans, [{"lead_id": "l1", "decision": "CONFIRM_BUSINESS_READY", "evidence_checked": "no", "artisan_checked": "no", "consent_status": "NON_DEMANDÉ"}])
        self.assertEqual(leads[0]["qualification_status"], "TO_VALIDATE")
        self.assertIn("evidence_checked != yes", leads[0]["human_validation_reason"])
        self.assertIn("artisan_checked != yes", leads[0]["human_validation_reason"])
        warnings = apply_human_confirmations(leads, artisans, [{"lead_id": "unknown", "decision": "CONFIRM_BUSINESS_READY", "evidence_checked": "yes", "artisan_checked": "yes", "consent_status": "NON_DEMANDÉ"}])
        self.assertTrue(any("lead inconnu" in w for w in warnings))

    def test_business_readiness_increase_only_when_real_validation(self):
        base_leads = [{"lead_id": "l1", "reality_status": "PARTIALLY_VERIFIED", "qualification_status": "TO_VALIDATE", "source_url": "https://real.tld/1"}]
        artisans = [{"source_kind": "OFFICIAL", "source_url": "https://artisan.tld"}]
        before = compute_business_readiness(base_leads, artisans)
        apply_human_confirmations(base_leads, artisans, [{"lead_id": "l1", "decision": "CONFIRM_BUSINESS_READY", "evidence_checked": "yes", "artisan_checked": "yes", "consent_status": "À_CLARIFIER"}])
        after = compute_business_readiness(base_leads, artisans)
        self.assertGreater(after["business_readiness_score"], before["business_readiness_score"])


if __name__ == "__main__":
    unittest.main()
