import json
import unittest
from pathlib import Path
from atlas.main import run_pipeline

class PipelineTests(unittest.TestCase):
    def test_v09_business_outputs(self):
        run_pipeline()
        self.assertTrue(Path('atlas/runtime/business/business_readiness.json').exists())
        self.assertTrue(Path('atlas/runtime/closer/call_scripts.md').exists())
        self.assertTrue(Path('atlas/scripts/business_check.sh').exists())

    def test_no_demo_in_business_ready(self):
        run_pipeline()
        data=json.loads(Path('atlas/runtime/export/leads_ranked.json').read_text(encoding='utf-8'))['leads']
        ready=[l for l in data if l.get('qualification_status')=='BUSINESS_READY']
        self.assertTrue(all(l.get('reality_status')!='DEMO' for l in ready))

    def test_caps_and_intent_guards(self):
        run_pipeline()
        data=json.loads(Path('atlas/runtime/export/leads_ranked.json').read_text(encoding='utf-8'))['leads']
        for l in data:
            if l.get('intent_type') in {'DIRECTORY_PAGE','ARTISAN_AD'}:
                self.assertNotEqual(l.get('qualification_status'),'BUSINESS_READY')

if __name__ == '__main__':
    unittest.main()
