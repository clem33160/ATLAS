import json
from pathlib import Path
import unittest

from atlas.main import run_pipeline


class PipelineTests(unittest.TestCase):
    def test_pipeline_outputs(self):
        result = run_pipeline()
        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["leads_processed"], 4)

        report = Path(result["report"])
        export = Path(result["export"])
        self.assertTrue(report.exists())
        self.assertTrue(export.exists())

        payload = json.loads(export.read_text(encoding="utf-8"))
        self.assertGreaterEqual(payload[0]["score"], payload[-1]["score"])
        self.assertIn("matched_artisan", payload[0])


if __name__ == "__main__":
    unittest.main()
