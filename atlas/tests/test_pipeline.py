import csv
import json
import unittest
from pathlib import Path

from atlas.main import (
    category_from_score,
    deduplicate_leads,
    load_csv,
    load_json,
    normalize_lead,
    run_pipeline,
    score_lead,
)


class PipelineTests(unittest.TestCase):
    def test_import_json_and_csv(self):
        json_rows = load_json(Path("atlas/inbox/leads_manual_example.json"))
        csv_rows = load_csv(Path("atlas/inbox/leads_manual_example.csv"))
        self.assertGreaterEqual(len(json_rows), 1)
        self.assertGreaterEqual(len(csv_rows), 1)

    def test_normalization_and_scoring(self):
        lead = normalize_lead({"title": "Test", "city": "lyon", "trade_hint": "renovation", "budget_eur": "5000€", "urgency": "urgent", "confidence": 0.8}, 1)
        score = score_lead(lead, {"Lyon": 1.2}, [{"trade": "rénovation", "cities": ["Lyon"], "capacity": 1}])
        self.assertEqual(lead["city"], "Lyon")
        self.assertEqual(lead["trade_hint"], "rénovation")
        self.assertEqual(lead["budget_eur"], 5000)
        self.assertEqual(lead["urgency"], "high")
        self.assertLessEqual(score, 100)

    def test_categories(self):
        self.assertEqual(category_from_score(20), "PETIT")
        self.assertEqual(category_from_score(45), "MOYEN")
        self.assertEqual(category_from_score(70), "GROS")
        self.assertEqual(category_from_score(90), "TITAN")

    def test_deduplication(self):
        leads = [
            normalize_lead({"id": "a", "title": "Fuite cuisine urgente", "city": "Lyon", "trade_hint": "plomberie", "budget_eur": 2000}, 1),
            normalize_lead({"id": "b", "title": "Urgente fuite cuisine", "city": "Lyon", "trade_hint": "plomberie", "budget_eur": 2200}, 2),
        ]
        unique, dup = deduplicate_leads(leads)
        self.assertEqual(len(unique), 1)
        self.assertEqual(len(dup), 1)

    def test_pipeline_outputs_and_exports(self):
        result = run_pipeline()
        self.assertEqual(result["status"], "ok")
        report = Path(result["report"])
        export_json = Path(result["export"])
        export_csv = Path(result["export_csv"])
        run_summary = Path(result["execution_summary"])
        self.assertTrue(report.exists())
        self.assertTrue(export_json.exists())
        self.assertTrue(export_csv.exists())
        self.assertTrue(run_summary.exists())

        payload = json.loads(export_json.read_text(encoding="utf-8"))
        self.assertIn("leads", payload)
        self.assertIn("duplicates", payload)
        self.assertGreaterEqual(payload["leads"][0]["score"], payload["leads"][-1]["score"])

        with export_csv.open("r", encoding="utf-8", newline="") as fh:
            rows = list(csv.DictReader(fh))
        self.assertEqual(len(rows), len(payload["leads"]))
        self.assertIn("pipeline_status", rows[0])

        report_content = report.read_text(encoding="utf-8")
        self.assertIn("Rapport V0.5", report_content)
        self.assertIn("Résumé exécutif", report_content)
        self.assertIn("Doublons détectés", report_content)

    def test_termux_compat(self):
        self.assertTrue(Path("atlas/scripts/run.sh").exists())
        self.assertTrue(Path("atlas/scripts/test.sh").exists())


if __name__ == "__main__":
    unittest.main()
