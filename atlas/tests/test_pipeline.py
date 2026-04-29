import json
import unittest
from pathlib import Path
from atlas.main import run_pipeline, load_csv, load_json
from atlas.sources.http_fetcher import extract_text_from_html

class PipelineTests(unittest.TestCase):
    def test_import_leads_json_csv(self):
        self.assertGreaterEqual(len(load_json(Path('atlas/inbox/leads_manual_example.json'))), 1)
        self.assertGreaterEqual(len(load_csv(Path('atlas/inbox/leads_manual_example.csv'))), 1)

    def test_import_artisans_examples(self):
        self.assertTrue(Path('atlas/inbox/artisans_manual.example.csv').exists())
        self.assertTrue(Path('atlas/inbox/artisans_manual.example.json').exists())

    def test_extract_from_fixture_html(self):
        html = Path('atlas/examples/html/chantier_plomberie_urgent.example.html').read_text(encoding='utf-8')
        txt = extract_text_from_html(html)
        self.assertIn('plomberie', txt.lower())

    def test_pipeline_outputs_v07(self):
        result = run_pipeline()
        self.assertEqual(result['status'], 'ok')
        for p in [
            'atlas/runtime/evidence/source_fetch_log.json',
            'atlas/runtime/evidence/source_fetch_errors.json',
            'atlas/runtime/reports/lead_report.md',
            'atlas/runtime/closer/daily_call_sheet.md',
            'atlas/runtime/export/leads_ranked.json',
            'atlas/runtime/export/leads_ranked.csv',
            'atlas/runtime/crm/next_actions.json',
            'atlas/runtime/matching/matches.json',
        ]:
            self.assertTrue(Path(p).exists(), p)
        self.assertIn('Rapport V0.7', Path('atlas/runtime/reports/lead_report.md').read_text(encoding='utf-8'))

    def test_termux_compat(self):
        self.assertTrue(Path('atlas/scripts/run.sh').exists())
        self.assertTrue(Path('atlas/scripts/test.sh').exists())

if __name__ == '__main__':
    unittest.main()
