import json
import unittest
from pathlib import Path

from atlas.main import category_from_score, load_csv, load_json, normalize_lead, run_pipeline


class PipelineTests(unittest.TestCase):
    def test_import_json_and_csv(self):
        self.assertGreaterEqual(len(load_json(Path('atlas/inbox/leads_manual_example.json'))), 1)
        self.assertGreaterEqual(len(load_csv(Path('atlas/inbox/leads_manual_example.csv'))), 1)

    def test_normalization(self):
        lead = normalize_lead({'city': '', 'trade_hint': '', 'budget_eur': ''}, 1)
        self.assertIn('city', lead['missing_fields'])
        self.assertIn('trade_hint', lead['missing_fields'])
        self.assertEqual(lead['evidence_status'], 'PARTIEL')

    def test_categories(self):
        self.assertEqual(category_from_score(30), 'FAIBLE')
        self.assertEqual(category_from_score(45), 'PETIT')
        self.assertEqual(category_from_score(60), 'MOYEN')
        self.assertEqual(category_from_score(80), 'GROS')
        self.assertEqual(category_from_score(90), 'TITAN')

    def test_pipeline_outputs(self):
        result = run_pipeline()
        self.assertEqual(result['status'], 'ok')
        paths = [
            'atlas/runtime/reports/lead_report.md',
            'atlas/runtime/export/leads_ranked.json',
            'atlas/runtime/export/leads_ranked.csv',
            'atlas/runtime/evidence/evidence_log.json',
            'atlas/runtime/matching/matches.json',
            'atlas/runtime/crm/leads_history.json',
            'atlas/runtime/closer/daily_call_sheet.md',
            'atlas/runtime/closer/daily_call_sheet.csv',
        ]
        for p in paths:
            self.assertTrue(Path(p).exists(), p)
        report = Path('atlas/runtime/reports/lead_report.md').read_text(encoding='utf-8')
        self.assertIn('Rapport V0.6', report)

    def test_termux_compat(self):
        self.assertTrue(Path('atlas/scripts/run.sh').exists())
        self.assertTrue(Path('atlas/scripts/test.sh').exists())


if __name__ == '__main__':
    unittest.main()
