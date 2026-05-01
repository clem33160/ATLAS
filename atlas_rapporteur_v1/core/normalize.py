#!/usr/bin/env python3
import datetime as dt, hashlib, json, re, sys
from pathlib import Path

def parse_amount(text):
    if not text: return None
    m = re.search(r'(\d[\d\s.,]{2,})', str(text))
    if not m: return None
    raw = m.group(1).replace(' ','').replace(',','.')
    try: return int(float(raw))
    except: return None

def size(amount):
    if amount is None: return 'A_VERIFIER'
    if amount < 10000: return 'PETIT'
    if amount < 50000: return 'MOYEN'
    if amount < 250000: return 'GROS'
    return 'TITAN'

inp,out=sys.argv[1],sys.argv[2]
Path(out).parent.mkdir(parents=True,exist_ok=True)
today=dt.date.today()
with open(inp,encoding='utf-8') as f, open(out,'w',encoding='utf-8') as o:
    for line in f:
        if not line.strip(): continue
        r=json.loads(line)
        p=(r.get('published_date') or str(today))[:10]
        try: age=(today-dt.date.fromisoformat(p)).days
        except: age=999
        amt=parse_amount(r.get('amount_text'))
        lead_id=hashlib.sha1((r.get('source_id','')+r.get('url','')).encode()).hexdigest()[:16]
        n={"lead_id":lead_id,"source_id":r.get('source_id','unknown'),"source_name":r.get('source_name','unknown'),"title":r.get('title','')[:180],"url":r.get('url',''),"published_date":p,"age_days":age,"domain":"A_VERIFIER","amount_eur":amt,"amount_status":"OK" if amt else "A_VERIFIER","commission_rate":5,"commission_eur": round(amt*0.05,2) if amt else None,"size":size(amt),"score":0,"score_reasons":[],"proof":r.get('url',''),"human_validation_required":True,"auto_contact":False,"verdict":"A_VERIFIER","buyer":r.get('buyer',''),"location":r.get('location','')}
        o.write(json.dumps(n,ensure_ascii=False)+"\n")
