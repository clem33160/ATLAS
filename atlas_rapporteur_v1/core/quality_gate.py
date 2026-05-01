#!/usr/bin/env python3
import json,sys
policy=json.load(open(sys.argv[3],encoding='utf-8'))
rej=policy['reject_url_patterns']
with open(sys.argv[1],encoding='utf-8') as f, open(sys.argv[2],'w',encoding='utf-8') as o:
  for l in f:
    r=json.loads(l);u=r.get('url','').lower();ver='A_VERIFIER'
    if not u or any(p in u for p in rej): ver='A_REJETER'
    r['verdict']=ver; o.write(json.dumps(r,ensure_ascii=False)+"\n")
