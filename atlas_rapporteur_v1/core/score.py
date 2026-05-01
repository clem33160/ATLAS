#!/usr/bin/env python3
import json,sys
pol=json.load(open(sys.argv[3],encoding='utf-8'));w=pol['weights'];caps=pol['caps']
with open(sys.argv[1],encoding='utf-8') as f, open(sys.argv[2],'w',encoding='utf-8') as o:
  for l in f:
    r=json.loads(l);re=[];s=0
    if r['source_id']=='boamp': s+=w['source_reliability']; re+=['source officielle']
    fr=max(0,w['freshness']-max(0,r['age_days'])*2); s+=fr
    if r['domain']!='A_VERIFIER': s+=w['domain_match']; re+=['domaine classifie']
    if r.get('amount_eur'): s+=w['amount_confidence']; re+=['montant detecte']
    if r.get('url'): s+=w['proof_url']
    if r.get('location'): s+=w['location']
    if r.get('buyer'): s+=w['buyer_context']
    s += w['human_action'] + w['difficulty'] + w['conversion_probability']
    if not r.get('url'): s=min(s,caps['without_proof'])
    if not r.get('amount_eur'): s=min(s,caps['without_amount'])
    if r['domain']=='A_VERIFIER': s=min(s,caps['fuzzy_domain'])
    if r.get('verdict')=='A_REJETER': s=0
    r['score']=max(0,min(100,int(s))); r['score_reasons']=re
    if r['verdict']!='A_REJETER' and r['score']>=65: r['verdict']='A_APPELER_APRES_VERIFICATION'
    o.write(json.dumps(r,ensure_ascii=False)+"\n")
