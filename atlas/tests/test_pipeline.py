import unittest
from pathlib import Path
from atlas.main import run_pipeline

class PipelineTests(unittest.TestCase):
    def test_v08_outputs(self):
        run_pipeline()
        self.assertTrue(Path('atlas/config/real_sources.yaml').exists())
        self.assertTrue(Path('atlas/runtime/export/real_leads_only.csv').exists())
        self.assertTrue(Path('atlas/runtime/export/artisans_ranked.csv').exists())
        self.assertIn('Rapport V0.8', Path('atlas/runtime/reports/lead_report.md').read_text(encoding='utf-8'))
        sheet=Path('atlas/runtime/closer/daily_call_sheet.md').read_text(encoding='utf-8')
        self.assertIn('À appeler aujourd’hui - leads réels seulement', sheet)
        self.assertIn('Démo uniquement - ne pas appeler', sheet)

    def test_private_sources_disabled(self):
        y=Path('atlas/config/real_sources.yaml').read_text(encoding='utf-8')
        self.assertIn('source_id: pagesjaunes', y)
        self.assertIn('collection_mode: disabled', y)

    def test_source_audit_exists(self):
        self.assertTrue(Path('atlas/scripts/source_audit.sh').exists())

if __name__ == '__main__':
    unittest.main()
