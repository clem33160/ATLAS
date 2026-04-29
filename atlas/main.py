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
def is_demo_url(url:str)->bool: return 'example.' in (url or '').lower()

def parse_source_urls():
    seen=set(); items=[]
    p=INBOX/'source_urls.txt'
    if not p.exists(): return items
    for l in p.read_text(encoding='utf-8').splitlines():
        l=l.strip()
        if not l or l.startswith('#'): continue
        parts=l.split('|')
        row={'source_id':'manual','url':'','note':'','country':'','city_hint':'','trade_hint':''}
        if len(parts)==1: row['url']=parts[0]
        else:
            row.update({'source_id':parts[0],'url':parts[1],'note':parts[2] if len(parts)>2 else '', 'country':parts[3] if len(parts)>3 else '', 'city_hint':parts[4] if len(parts)>4 else '', 'trade_hint':parts[5] if len(parts)>5 else ''})
        if row['url'] not in seen: seen.add(row['url']); items.append(row)
    return items

def lead_score(lead, has_artisan=False):
    s=0
    s += 20 if lead.get('budget_mid',0)>=10000 else 10
    s += 10 if lead.get('urgency')=='high' else 5
    s += 10
    s += 10 if len(lead.get('description',''))>40 else 4
    s += 20 if lead.get('source_url') else 0
    s += 10 if lead.get('trade') else 0
    s += 5 if lead.get('city') else 0
    s += 10 if has_artisan else 0
    s += 5 if lead.get('intent_type') in {'CLIENT_REQUEST','PUBLIC_MARKET'} else 0
    caps=[]
    if lead['reality_status']=='DEMO': s=min(s,60); caps.append('DEMO max 60')
    if lead['reality_status']=='MANUAL' and not lead.get('source_url'): s=min(s,65); caps.append('MANUAL sans URL max 65')
    if lead['reality_status']=='COLLECTED_FROM_URL' and lead.get('intent_type')=='GENERIC_PAGE': s=min(s,55); caps.append('URL générique max 55')
    if lead['reality_status']=='COLLECTED_FROM_URL' and lead.get('intent_type')=='UNKNOWN': s=min(s,50); caps.append('intent UNKNOWN max 50')
    lead['score_total']=s; lead['score_caps_applied']=caps
    lead['qualification_status']='BUSINESS_READY' if all([lead.get('source_url'),lead.get('evidence_summary'),lead.get('city'),lead.get('trade'),lead.get('intent_type') in {'CLIENT_REQUEST','PUBLIC_MARKET'},s>=70,has_artisan]) else 'TO_VALIDATE'
    return lead

def run_pipeline(mode='run'):
    for d in ['reports','export','closer','crm','matching','evidence','artisans','business']: (RUN/d).mkdir(parents=True,exist_ok=True)
    artisans,warns=resolve_artisans(BASE)
    real_artisans=[a for a in artisans if a.get('source_kind')!='DEMO']
    leads=[]; cards=[]; fetch=[]; errors=[]
    for s in parse_source_urls():
        res=fetch_public_url(s['url'])
        if not res['ok']:
            errors.append({'url':s['url'],'error':res['error']}); continue
        text=normalize_web_text(extract_text_from_html(res['raw_html']))
        sig=extract_signals(text)
        rs='DEMO' if is_demo_url(s['url']) else 'COLLECTED_FROM_URL'
        if sig.get('city') and sig.get('trade'): rs='PARTIALLY_VERIFIED'
        card={'url':s['url'],'source_id':s['source_id'],'collected_at':now(),'http_status':res.get('http_status'),'fetch_status':'OK','raw_excerpt':safe_excerpt(text,240),'clean_excerpt':safe_excerpt(text,140),'detected_city':sig.get('city',''),'detected_trade':sig.get('trade',''),'detected_budget':sig.get('budget_mid',0),'detected_urgency':sig.get('urgency'),'confidence':0.7,'compliance_note':'no crawl/no post','extraction_errors':[],'human_review_required':True}
        cards.append(card); fetch.append({'source_id':s['source_id'],'url':s['url'],'collected_at':now()})
        lead={'lead_id':f'url-{len(leads)+1}','title':f"Lead {sig.get('trade') or 'à qualifier'}",'description':safe_excerpt(text,220),'country':sig.get('country',''),'city':sig.get('city',''),'zip_code':sig.get('zip_code',''),'trade':sig.get('trade',''),'trade_family':sig.get('trade_family',''),'intent_type':sig.get('intent_type','UNKNOWN'),'reality_status':rs,'source_id':s['source_id'],'source_url':s['url'],'collected_at':now(),'raw_excerpt':safe_excerpt(text,160),'evidence_summary':safe_excerpt(text,100),'evidence_quality':'MEDIUM','budget_low':sig.get('budget_low',0),'budget_mid':sig.get('budget_mid',0),'budget_high':sig.get('budget_high',0),'budget_status':sig.get('budget_status'),'urgency':sig.get('urgency'),'freshness_days':0,'confidence':0.7,'risk_flags':[],'missing_fields':[],'business_priority':'MOYEN','pipeline_status':'NEW','human_review_required':True}
        leads.append(lead)
    for l in leads:
        has_artisan=any(a.get('source_kind')!='DEMO' for a in artisans)
        lead_score(l,has_artisan=has_artisan)
    business_ready=[l for l in leads if l['qualification_status']=='BUSINESS_READY' and l['reality_status']!='DEMO']
    real=[l for l in leads if l['reality_status']!='DEMO']
    (RUN/'export'/'leads_ranked.json').write_text(json.dumps({'leads':leads},ensure_ascii=False,indent=2),encoding='utf-8')
    (RUN/'evidence'/'url_evidence_cards.json').write_text(json.dumps(cards,ensure_ascii=False,indent=2),encoding='utf-8')
    (RUN/'evidence'/'source_fetch_log.json').write_text(json.dumps(fetch,ensure_ascii=False,indent=2),encoding='utf-8')
    (RUN/'evidence'/'source_fetch_errors.json').write_text(json.dumps(errors,ensure_ascii=False,indent=2),encoding='utf-8')
    (RUN/'evidence'/'url_evidence_cards.md').write_text('\n'.join(['# URL Evidence Cards']+[f"- {c['url']} | {c['detected_city']} | {c['detected_trade']}" for c in cards])+'\n',encoding='utf-8')
    br_score=round(min(10.0, (len(real)>0)*2 + (len(cards)>0)*1.5 + (len([l for l in leads if l.get('budget_mid',0)>0])>0)*1.5 + (len(real_artisans)>0)*1.5 + (len(business_ready)>0)*1 + 0.8 + 0.8 + 0.7),1)
    reasons=[]
    if not business_ready: reasons.append('0 lead BUSINESS_READY')
    if not real_artisans: reasons.append('0 artisan vérifiable')
    if len(cards)<1: reasons.append('preuves URL insuffisantes')
    br={'business_readiness_score':br_score,'max_score_with_current_data':8.3 if not business_ready else 10.0,'blocking_reasons':reasons,'actions':['ajouter 20 URLs publiques ciblées','ajouter artisans officiels vérifiés','importer retours d’appels','confirmer humainement les meilleurs leads']}
    (RUN/'business'/'business_readiness.json').write_text(json.dumps(br,ensure_ascii=False,indent=2),encoding='utf-8')
    (RUN/'business'/'business_readiness.md').write_text(f"# Business Readiness\n\nBusiness Readiness Score : {br_score}/10\n\n## Pourquoi pas 10/10\n"+'\n'.join([f'- {x}' for x in reasons or ['Aucun blocage']])+"\n\n## Actions\n"+'\n'.join([f'- {x}' for x in br['actions']])+"\n",encoding='utf-8')
    call=['# Daily Call Sheet V0.9','', '## 1. Résumé business du jour', f'- Leads collectés: {len(leads)}','## 2. Business Readiness Score',f'- {br_score}/10','## 3. À appeler maintenant - BUSINESS_READY seulement']
    call += [f"- {l['lead_id']} | {l['city']} | {l['trade']}" for l in business_ready] or ['Aucun lead business-ready aujourd’hui. Ne pas appeler. Ajouter des URLs précises ou valider manuellement les leads.']
    call += ['', '## 4. À valider avant appel'] + [f"- {l['lead_id']}" for l in real if l['qualification_status']!='BUSINESS_READY']
    call += ['', '## 5. Leads réels mais incomplets', f"- {len([l for l in real if not l.get('city') or not l.get('trade')])}", '## 6. Leads rejetés / non exploitables','- Aucun', '## 7. Démo uniquement - ne pas appeler','- Aucun', '## 8. Artisans réels recommandés']
    call += [f"- {a.get('name','Inconnu')}" for a in real_artisans] or ['- Aucun']
    call += ['', '## 9. Artisans à vérifier'] + [f"- {w.get('name')}" for w in warns] + ['', '## 10. Scripts d’appel','Voir call_scripts.md','## 11. Questions obligatoires','- Budget? Délai? Consentement?','## 12. Consentement transmission','- Obtenir accord explicite','## 13. Prochaines actions','- Compléter CRM et confirmations humaines']
    (RUN/'closer'/'daily_call_sheet.md').write_text('\n'.join(call)+'\n',encoding='utf-8')
    (RUN/'closer'/'call_scripts.md').write_text('# Scripts d\'appel business\n- Script artisan\n- Script client (si légalement possible)\n- Vérification besoin\n- Consentement transmission\n- Refus poli\n- Relance\n- Demande commission\n',encoding='utf-8')
    (RUN/'crm'/'pipeline_summary.json').write_text(json.dumps({'to_call':len(business_ready),'to_validate':len(real)-len(business_ready),'to_followup':0},indent=2),encoding='utf-8')
    (RUN/'crm'/'next_actions.json').write_text(json.dumps({'actions':br['actions']},indent=2),encoding='utf-8')
    (RUN/'crm'/'deal_potential.json').write_text(json.dumps({'deals_potentiels':len(business_ready),'commission_basse':0,'commission_moyenne':0,'commission_haute':0},indent=2),encoding='utf-8')
    (RUN/'crm'/'call_outcomes_summary.md').write_text('Aucun appel réel.\n',encoding='utf-8')

    (RUN/'reports'/'lead_report.md').write_text('# Atlas Rapporteur d’Affaires — Rapport V0.9\n\n' +
        f'Leads totaux: {len(leads)}\nLeads BUSINESS_READY: {len(business_ready)}\n',encoding='utf-8')
    (RUN/'artisans'/'artisans_ranked.json').write_text(json.dumps({'artisans':artisans},ensure_ascii=False,indent=2),encoding='utf-8')
    (RUN/'artisans'/'artisans_ranked.csv').write_text('name,source_kind,source_url\n'+'\n'.join([f"{a.get('name','')},{a.get('source_kind','')},{a.get('source_url','')}" for a in artisans]),encoding='utf-8')
    (RUN/'artisans'/'artisan_warnings.md').write_text('\n'.join(['# Artisan warnings']+[f"- {w.get('name','')} : {w.get('warning','')}" for w in warns]),encoding='utf-8')
    (RUN/'matching'/'business_matches.json').write_text(json.dumps({'matches':[]},indent=2),encoding='utf-8')
    (RUN/'matching'/'business_matches.md').write_text('# Business Matches\nAucun match fort.\n',encoding='utf-8')

    return {'status':'ok'}

if __name__=='__main__':
    run_pipeline()
    print('ATLAS RAPPORTEUR D’AFFAIRES — V0.9')
