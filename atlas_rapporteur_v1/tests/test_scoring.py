#!/usr/bin/env python3
import json,glob
p=sorted(glob.glob('atlas_rapporteur_v1/runtime/reports/report_*.jsonl'))[-1]
for l in open(p,encoding='utf-8'):
 r=json.loads(l)
 if r['score']==100:
  assert r.get('url') and r.get('amount_eur') and r.get('domain')!='A_VERIFIER'
print('ok scoring')
