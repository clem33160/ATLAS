#!/usr/bin/env python3
import json,sys
rate=0.05
with open(sys.argv[1],encoding='utf-8') as f, open(sys.argv[2],'w',encoding='utf-8') as o:
  for l in f:
    r=json.loads(l);a=r.get('amount_eur')
    r['commission_rate']=5; r['commission_eur']= round(a*rate,2) if isinstance(a,(int,float)) else None
    o.write(json.dumps(r,ensure_ascii=False)+"\n")
