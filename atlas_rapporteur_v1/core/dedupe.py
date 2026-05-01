#!/usr/bin/env python3
import json, sys
seen=set()
with open(sys.argv[1],encoding='utf-8') as f, open(sys.argv[2],'w',encoding='utf-8') as o:
  for l in f:
    if not l.strip(): continue
    r=json.loads(l); k=(r.get('source_id'),r.get('url'))
    if k in seen: continue
    seen.add(k); o.write(json.dumps(r,ensure_ascii=False)+"\n")
