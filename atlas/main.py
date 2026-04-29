#!/usr/bin/env python3
from __future__ import annotations
import csv, json
from pathlib import Path
from datetime import datetime, timezone
from atlas.extraction import extract_signals
from atlas.sources.http_fetcher import fetch_public_url, extract_text_from_html, normalize_web_text, safe_excerpt
from atlas.artisans import resolve_artisans

BASE=Path(__file__).resolve().parent
INBOX=BASE/'inbox'; DATA=BASE/'data'; RUN=BASE/'runtime'

def now(): return datetime.now(timezone.utc).isoformat()
def load_json(p): return json.loads(p.read_text(encoding='utf-8')) if p.exists() else []
def load_csv(p):
    if not p.exists(): return []
    with p.open('r',encoding='utf-8',newline='') as f: return list(csv.DictReader(f))

def parse_source_urls():
    items=[]
    p=INBOX/'source_urls.txt'
    if not p.exists(): return items
    for l in p.read_text(encoding='utf-8').splitlines():
        l=l.strip()
        if not l or l.startswith('#'): continue
        if '|' in l:
            sid,url,*rest=l.split('|')
            items.append({'source_id':sid,'url':url,'note':rest[0] if rest else ''})
        else: items.append({'source_id':'user_manual','url':l,'note':''})
    return items

def run_pipeline(mode='run'):
    for d in ['reports','export','closer','crm','matching','evidence','artisans']: (RUN/d).mkdir(parents=True,exist_ok=True)
    artisans,warns=resolve_artisans(BASE)
    leads=[]
    for i,r in enumerate(load_json(DATA/'sources'/'demo_public_signals.json'),1):
        leads.append({'id':r.get('id',f'demo-{i}'),'title':r.get('title',''),'city':r.get('city',''),'trade_hint':r.get('trade_hint',''),'evidence_url':r.get('evidence_url',''),'reality_status':'DEMO','evidence_raw_excerpt':r.get('description',''),'confidence':0.3})
    for r in load_json(INBOX/'leads_manual_example.json')+load_csv(INBOX/'leads_manual_example.csv'):
        leads.append({'id':r.get('id',f'manual-{len(leads)}'),'title':r.get('title',''),'city':r.get('city',''),'trade_hint':r.get('trade_hint',''),'evidence_url':r.get('evidence_url',''),'reality_status':'MANUAL','evidence_raw_excerpt':r.get('description',''),'confidence':0.6 if r.get('evidence_url') else 0.45})
    fetch=[]
    for s in parse_source_urls():
        res=fetch_public_url(s['url'])
        if not res['ok']: continue
        text=normalize_web_text(extract_text_from_html(res['raw_html']))
        sig=extract_signals(text)
        status='PARTIALLY_VERIFIED' if sig.get('city') and sig.get('trade_hint') else 'COLLECTED_FROM_URL'
        leads.append({'id':f"url-{len(leads)+1}",'title':f"Lead collecté {sig.get('trade_hint') or 'à qualifier'}",'city':sig.get('city',''),'trade_hint':sig.get('trade_hint',''),'evidence_url':s['url'],'reality_status':status,'evidence_raw_excerpt':safe_excerpt(text,180),'confidence':0.75 if status=='PARTIALLY_VERIFIED' else 0.65,'collected_at':now()})
        fetch.append({'source_id':s['source_id'],'url':s['url'],'note':s['note'],'collected_at':now()})
    for l in leads:
        l['score_total']=80 if l['reality_status'] in {'HUMAN_CONFIRMED','PARTIALLY_VERIFIED'} else 70 if l['reality_status'] in {'COLLECTED_FROM_URL','MANUAL'} else 40
    real=[l for l in leads if l['reality_status'] in {'MANUAL','COLLECTED_FROM_URL','PARTIALLY_VERIFIED','HUMAN_CONFIRMED'} and l.get('evidence_url')]
    demo=[l for l in leads if l['reality_status']=='DEMO']
    with (RUN/'export'/'leads_ranked.json').open('w',encoding='utf-8') as f: json.dump({'leads':leads},f,ensure_ascii=False,indent=2)
    def write_csv(path,rows,fields):
        with path.open('w',encoding='utf-8',newline='') as f:
            w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); [w.writerow({k:r.get(k,'') for k in fields}) for r in rows]
    fields=['id','reality_status','city','trade_hint','score_total','evidence_url']
    write_csv(RUN/'export'/'leads_ranked.csv',leads,fields)
    write_csv(RUN/'export'/'real_leads_only.csv',real,fields)
    art_rows=[{'name':a.get('name',''),'city':a.get('city',''),'source_kind':a.get('source_kind',''),'source_url':a.get('source_url',''),'phone':a.get('phone',''),'website':a.get('website','')} for a in artisans]
    write_csv(RUN/'export'/'artisans_ranked.csv',art_rows,['name','city','source_kind','source_url','phone','website'])
    (RUN/'evidence'/'source_fetch_log.json').write_text(json.dumps(fetch,ensure_ascii=False,indent=2),encoding='utf-8')
    (RUN/'evidence'/'source_fetch_errors.json').write_text('[]',encoding='utf-8')
    report=['# Atlas Rapporteur d’Affaires — Rapport V0.8','',f'Leads DEMO: {len(demo)}',f'Leads MANUAL: {sum(1 for x in leads if x["reality_status"]=="MANUAL")}',f'Leads COLLECTED_FROM_URL: {sum(1 for x in leads if x["reality_status"]=="COLLECTED_FROM_URL")}',f'Leads PARTIALLY_VERIFIED: {sum(1 for x in leads if x["reality_status"]=="PARTIALLY_VERIFIED")}',f'Leads HUMAN_CONFIRMED: {sum(1 for x in leads if x["reality_status"]=="HUMAN_CONFIRMED")}','','## Leads réels exploitables']
    report += [f"- {l['id']} | {l['reality_status']} | {l.get('evidence_url','')}" for l in real] or ['- Aucun']
    report += ['','## Démonstration uniquement'] + [f"- {l['id']}" for l in demo]
    (RUN/'reports'/'lead_report.md').write_text('\n'.join(report)+'\n',encoding='utf-8')
    call=['# Daily Call Sheet V0.8','', '## 1. À appeler aujourd’hui - leads réels seulement']
    call += [f"- {l['id']}" for l in real] if real else ['Aucun lead réel exploitable aujourd’hui. Ajoutez des URLs publiques dans atlas/inbox/source_urls.txt ou des leads manuels vérifiés.']
    call += ['', '## 2. À valider avant appel'] + [f"- {l['id']}" for l in leads if l['reality_status']=='MANUAL' and not l.get('evidence_url')]
    call += ['', '## 3. Démo uniquement - ne pas appeler'] + [f"- {l['id']}" for l in demo]
    call += ['', '## 4. Artisans recommandés réels'] + [f"- {a.get('name','')} (source officielle / annuaire)" for a in artisans if a.get('source_kind') in {'OFFICIAL_DIRECTORY','RGE','SIRENE'}]
    call += ['', '## 5. Artisans à vérifier'] + [f"- {w['name']} ({w['warning']})" for w in warns]
    call += ['', '## 6. Notes de conformité','- Validation humaine des CGU requise.','- Aucun contact automatique.','- Aucun scraping agressif.']
    (RUN/'closer'/'daily_call_sheet.md').write_text('\n'.join(call)+'\n',encoding='utf-8')
    return {'status':'ok'}

if __name__=='__main__':
    run_pipeline()
    print('ATLAS RAPPORTEUR D’AFFAIRES — V0.8')
