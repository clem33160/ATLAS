#!/usr/bin/env python3
import json,glob
p=sorted(glob.glob('atlas_rapporteur_v1/runtime/reports/report_*.jsonl'))[-1]
for l in open(p,encoding='utf-8'):
 r=json.loads(l);u=r.get('url','').lower();
 assert u, 'lead sans URL'
 assert not any(x in u for x in ['/login','/api','/aide','/help']), 'url interdite'
print('ok quality gate')
