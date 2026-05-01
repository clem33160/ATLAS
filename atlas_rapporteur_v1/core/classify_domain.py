#!/usr/bin/env python3
import json,sys
conf=json.load(open(sys.argv[3],encoding='utf-8'))
kw=conf['keywords']
with open(sys.argv[1],encoding='utf-8') as f, open(sys.argv[2],'w',encoding='utf-8') as o:
  for l in f:
    r=json.loads(l); t=(r.get('title')+' '+r.get('buyer','')).lower(); d='A_VERIFIER'
    for dom,arr in kw.items():
      if any(k in t for k in arr): d=dom; break
    r['domain']=d; o.write(json.dumps(r,ensure_ascii=False)+"\n")
