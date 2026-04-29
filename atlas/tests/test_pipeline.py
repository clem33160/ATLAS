import csv
import json
from pathlib import Path
import unittest

from atlas.main import run_pipeline


class PipelineTests(unittest.TestCase):
    def test_pipeline_outputs(self):
        result = run_pipeline()
        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["leads_processed"], 6)

        report = Path(result["report"])
        export_json = Path(result["export"])
        export_csv = Path(result["export_csv"])
        self.assertTrue(report.exists())
        self.assertTrue(export_json.exists())
        self.assertTrue(export_csv.exists())

        payload = json.loads(export_json.read_text(encoding="utf-8"))
        self.assertGreaterEqual(payload[0]["score"], payload[-1]["score"])
        self.assertIn("matched_artisan", payload[0])
        self.assertIn("category", payload[0])
        self.assertLessEqual(payload[0]["score"], 100)
        self.assertIn(payload[0]["category"], {"PETIT", "MOYEN", "GROS", "TITAN"})

        with export_csv.open("r", encoding="utf-8", newline="") as fh:
            rows = list(csv.DictReader(fh))
        self.assertEqual(len(rows), len(payload))
        self.assertIn("id", rows[0])
        self.assertIn("category", rows[0])

        report_content = report.read_text(encoding="utf-8")
        self.assertIn("Rapport V0.3", report_content)
        self.assertIn("## Top 5 des leads", report_content)
        self.assertIn("Catégorie", report_content)


if __name__ == "__main__":
    unittest.main()
