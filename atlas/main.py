#!/usr/bin/env python3
from __future__ import annotations
import csv, json, re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from atlas.sources.http_fetcher import fetch_public_url, extract_text_from_html, normalize_web_text, safe_excerpt
from atlas.extraction import extract_signals

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
INBOX_DIR = BASE_DIR / "inbox"
RUNTIME_DIR = BASE_DIR / "runtime"

REALITY = {"DEMO","MANUAL","COLLECTED_FROM_URL","PARTIALLY_VERIFIED","HUMAN_CONFIRMED","ARCHIVED"}


def now_iso() -> str: return datetime.now(timezone.utc).isoformat()
def load_json(p: Path): return json.loads(p.read_text(encoding="utf-8")) if p.exists() else []
def load_csv(p: Path):
    if not p.exists(): return []
    with p.open("r", encoding="utf-8", newline="") as fh: return list(csv.DictReader(fh))


def parse_budget(v: Any) -> int:
    if isinstance(v,(int,float)): return int(v)
    m = re.sub(r"[^0-9]","",str(v or "")); return int(m) if m else 0


def collect_source_urls() -> tuple[list[dict], list[dict], bool]:
    log, errs = [], []
    online_ok = True
    for line in (INBOX_DIR/"source_urls.txt").read_text(encoding="utf-8").splitlines() if (INBOX_DIR/"source_urls.txt").exists() else []:
        url = line.strip()
        if not url or url.startswith("#"): continue
        rec = {"url":url,"collected_at":now_iso(),"source_type":"user_provided_url","compliance_note":"Validation humaine des conditions du site requise."}
        res = fetch_public_url(url)
        if not res["ok"]:
            rec.update({"fetch_status":"FAILED","http_status":res.get("http_status"),"raw_excerpt":"","normalized_text_excerpt":"","detected_trade_hints":[],"detected_city_hints":[],"detected_budget_hints":[],"detected_urgency_hints":[]})
            errs.append({"url":url,"error":res.get("error")}); online_ok=False
        else:
            text = extract_text_from_html(res["raw_html"])
            sig = extract_signals(text)
            rec.update({"fetch_status":"OK","http_status":res.get("http_status"),"raw_excerpt":safe_excerpt(res["raw_html"]),"normalized_text_excerpt":safe_excerpt(normalize_web_text(text)),"detected_trade_hints":[sig["trade_hint"]] if sig["trade_hint"] else [],"detected_city_hints":[sig["city"]] if sig["city"] else [],"detected_budget_hints":[sig["budget_eur"]] if sig["budget_eur"] else [],"detected_urgency_hints":[sig["urgency"]]})
        log.append(rec)
    return log, errs, online_ok


def score(lead, artisans):
    b={"budget_score":min(20,lead["budget_eur"]//1500),"urgency_score":15 if lead["urgency"]=="high" else 8,"clarity_score":min(10,len(lead["title"])//8),"evidence_score":20 if lead.get("evidence_url") else 8,"trade_profitability_score":10 if lead["trade_hint"] in {"rénovation","toiture","chauffage","électricité"} else 6,"location_score":5 if lead.get("city") else 0,"artisan_match_score":10 if any(lead["trade_hint"] in a.get("trades",[]) for a in artisans) else 2,"closing_probability_score":5 if lead["urgency"]=="high" else 2,"confidence_score":int(max(0,min(5,round(lead.get("confidence",0.4)*5))))}
    total=sum(b.values()); caps=[]
    if not lead.get("evidence_url"): caps.append("no_real_url_evidence_cap")
    if not lead.get("city"): total=min(total,50); caps.append("missing_city_cap_50")
    if not lead.get("trade_hint"): total=min(total,45); caps.append("missing_trade_cap_45")
    return total,b,caps

def cat(s): return "TITAN" if s>=85 else "GROS" if s>=70 else "MOYEN" if s>=55 else "PETIT" if s>=40 else "FAIBLE"

def run_pipeline(mode="run"):
    for d in ["reports","export","closer","crm","matching","evidence","outputs"]: (RUNTIME_DIR/d).mkdir(parents=True,exist_ok=True)
    artisans=load_json(DATA_DIR/"artisans"/"demo_artisans.json")
    artisans += [{**a,"reality_status":"MANUAL"} for a in load_csv(INBOX_DIR/"artisans_manual.csv")]
    artisans += [{**a,"reality_status":"MANUAL"} for a in load_json(INBOX_DIR/"artisans_manual.json")]
    for a in artisans: a.setdefault("reality_status","DEMO")

    leads=[]
    for i,r in enumerate(load_json(DATA_DIR/"sources"/"demo_public_signals.json"),1):
        leads.append({"id":r.get("id",f"demo-{i}"),"title":r.get("title",""),"description":r.get("description",""),"city":r.get("city",""),"zip_code":r.get("zip_code",""),"trade_hint":r.get("trade_hint",""),"budget_eur":parse_budget(r.get("budget_eur")),"urgency":r.get("urgency","medium"),"evidence_url":r.get("evidence_url",""),"reality_status":"DEMO","evidence_raw_excerpt":r.get("description",""),"evidence_summary":"Donnée démo","confidence":0.6,"evidence_status":"PARTIEL"})
    for r in load_json(INBOX_DIR/"leads_manual_example.json")+load_csv(INBOX_DIR/"leads_manual_example.csv"):
        leads.append({"id":r.get("id",f"manual-{len(leads)}"),"title":r.get("title",""),"description":r.get("description",""),"city":r.get("city",""),"zip_code":r.get("zip_code",""),"trade_hint":r.get("trade_hint",""),"budget_eur":parse_budget(r.get("budget_eur")),"urgency":r.get("urgency","medium"),"evidence_url":r.get("evidence_url",""),"reality_status":"MANUAL","evidence_raw_excerpt":r.get("description",""),"evidence_summary":"Saisie manuelle","confidence":0.55,"evidence_status":"PARTIEL"})

    fetch_log, fetch_err, online_ok = collect_source_urls()
    for e in fetch_log:
        if e["fetch_status"]!="OK": continue
        sig=extract_signals(e["normalized_text_excerpt"])
        rs="PARTIALLY_VERIFIED" if e["url"] and sig.get("city") and sig.get("trade_hint") else "COLLECTED_FROM_URL"
        leads.append({"id":f"url-{len(leads)+1}","title":f"Lead collecté {sig.get('trade_hint') or 'à qualifier'}","description":e["normalized_text_excerpt"],"city":sig.get("city",""),"zip_code":sig.get("zip_code",""),"trade_hint":sig.get("trade_hint",""),"budget_eur":sig.get("budget_eur",0) or 3000,"urgency":sig.get("urgency","medium"),"evidence_url":e["url"],"reality_status":rs,"evidence_raw_excerpt":e["raw_excerpt"],"evidence_summary":"Extrait collecté depuis URL publique fournie manuellement","confidence":0.65,"evidence_status":"CONFIRMÉ"})

    for l in leads:
        l["score_total"],l["score_breakdown"],l["score_caps_applied"]=score(l,artisans)
        l["category"]=cat(l["score_total"])
        l["top_score_reasons"]= [k for k,v in l["score_breakdown"].items() if v>=10][:3]
        l["risk_flags"]=[] if l.get("evidence_url") else ["preuve_insuffisante"]
    leads.sort(key=lambda x:x["score_total"],reverse=True)

    (RUNTIME_DIR/"evidence"/"source_fetch_log.json").write_text(json.dumps(fetch_log,ensure_ascii=False,indent=2),encoding="utf-8")
    (RUNTIME_DIR/"evidence"/"source_fetch_errors.json").write_text(json.dumps(fetch_err,ensure_ascii=False,indent=2),encoding="utf-8")
    (RUNTIME_DIR/"evidence"/"evidence_log.json").write_text(json.dumps([{k:l.get(k) for k in ["id","evidence_url","evidence_raw_excerpt","evidence_summary","reality_status"]} for l in leads],ensure_ascii=False,indent=2),encoding="utf-8")

    matches=[]
    for l in leads:
        c=[a for a in artisans if l.get("trade_hint") in a.get("trades",[])]
        c.sort(key=lambda x:(float(x.get("rating",0) or 0),int(x.get("reviews_count",0) or 0),float(x.get("confidence",0) or 0)),reverse=True)
        p=c[0] if c else {"name":"Aucun artisan","phone":"","website":"","reality_status":"DEMO"}
        l["artisan_recommended"]=p; l["artisan_alternatives"]=c[1:4]
        matches.append({"lead_id":l["id"],"primary_artisan":p,"alternatives":c[1:4],"matching_reason":"métier+confiance","matching_confidence":"MOYEN","warning":"artisan non vérifié" if p.get("reality_status")!="MANUAL" else ""})
    (RUNTIME_DIR/"matching"/"matches.json").write_text(json.dumps(matches,ensure_ascii=False,indent=2),encoding="utf-8")

    calls=load_csv(INBOX_DIR/"call_updates.csv")
    changes=[]; next_actions=[]
    for c in calls:
        st="NOUVEAU"
        if c.get("call_status")=="INTÉRESSÉ" and c.get("consent_status")=="ACCORD_TRANSMISSION": st="DEAL_POTENTIEL"
        elif c.get("call_status")=="PAS_INTÉRESSÉ": st="PERDU"
        elif c.get("call_status")=="À_RELANCER": st="À_RELANCER"
        elif c.get("call_status")=="SIGNÉ": st="SIGNÉ"
        changes.append({"lead_id":c.get("lead_id"),"pipeline_status":st})
        next_actions.append({"lead_id":c.get("lead_id"),"next_action_at":c.get("next_action_at",""),"notes":c.get("notes","")})
    (RUNTIME_DIR/"crm"/"call_log.json").write_text(json.dumps(calls,ensure_ascii=False,indent=2),encoding="utf-8")
    (RUNTIME_DIR/"crm"/"status_changes.json").write_text(json.dumps(changes,ensure_ascii=False,indent=2),encoding="utf-8")
    (RUNTIME_DIR/"crm"/"next_actions.json").write_text(json.dumps(next_actions,ensure_ascii=False,indent=2),encoding="utf-8")
    (RUNTIME_DIR/"crm"/"leads_history.json").write_text(json.dumps(leads,ensure_ascii=False,indent=2),encoding="utf-8")

    with (RUNTIME_DIR/"export"/"leads_ranked.json").open("w",encoding="utf-8") as f: json.dump({"leads":leads},f,ensure_ascii=False,indent=2)
    with (RUNTIME_DIR/"export"/"leads_ranked.csv").open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=["id","reality_status","city","trade_hint","score_total","category","evidence_url"]); w.writeheader(); [w.writerow({k:l.get(k,"") for k in w.fieldnames}) for l in leads]

    callables=[l for l in leads if l["category"] in {"GROS","TITAN","MOYEN"} and l.get("city") and l.get("trade_hint")]
    no_call=[l for l in leads if not (l.get("city") and l.get("trade_hint") and l.get("evidence_url"))]
    md=["# Atlas Rapporteur d’Affaires — Rapport V0.7","","## Résumé exécutif",f"- Leads traités: {len(leads)}",f"- DEMO: {sum(1 for l in leads if l['reality_status']=='DEMO')}",f"- MANUAL: {sum(1 for l in leads if l['reality_status']=='MANUAL')}",f"- COLLECTED_FROM_URL/PARTIALLY_VERIFIED: {sum(1 for l in leads if l['reality_status'] in {'COLLECTED_FROM_URL','PARTIALLY_VERIFIED'})}",f"- HUMAN_CONFIRMED: {sum(1 for l in leads if l['reality_status']=='HUMAN_CONFIRMED')}",f"- Leads avec URL: {sum(1 for l in leads if l.get('evidence_url'))}",f"- Leads sans URL: {sum(1 for l in leads if not l.get('evidence_url'))}",f"- Collecte URL réelle disponible: {'OUI' if online_ok else 'NON (fallback offline)'}",""]
    md += ["## Top 10 leads"]+[f"- {i}. {l['id']} | {l['reality_status']} | {l.get('city') or 'Inconnue'} | {l.get('trade_hint') or 'Inconnu'} | {l['score_total']} ({l['category']})" for i,l in enumerate(leads[:10],1)]
    md += ["","## Totaux par ville"]+[f"- {k or 'Inconnue'}: {v}" for k,v in Counter([l.get('city','') for l in leads]).items()]
    md += ["","## Totaux par métier"]+[f"- {k or 'Inconnu'}: {v}" for k,v in Counter([l.get('trade_hint','') for l in leads]).items()]
    md += ["","## Leads à appeler aujourd’hui"]+[f"- {l['id']}" for l in callables[:10]]+["","## Leads à ne pas appeler"]+[f"- {l['id']} (preuve insuffisante/ville/métier/source)" for l in no_call[:10]]
    (RUNTIME_DIR/"reports"/"lead_report.md").write_text("\n".join(md)+"\n",encoding="utf-8")

    c=["# Daily Call Sheet V0.7","","## Ordre d’appel recommandé aujourd’hui"]
    for i,l in enumerate(callables[:15],1): c += [f"### {i}. {l['id']}",f"- Statut réalité: {l['reality_status']}",f"- Ville: {l.get('city') or 'Inconnue'}",f"- Métier: {l.get('trade_hint') or 'Inconnu'}",f"- URL preuve: {l.get('evidence_url') or 'N/A'}",f"- Extrait preuve: {safe_excerpt(l.get('evidence_raw_excerpt',''),180)}",f"- Artisan recommandé: {l['artisan_recommended'].get('name','')}",f"- Téléphone artisan: {l['artisan_recommended'].get('phone','')}",f"- Site artisan: {l['artisan_recommended'].get('website','')}","- Consentement à demander: ACCORD_TRANSMISSION",""]
    c += ["## À ne pas appeler"]+[f"- {l['id']}" for l in no_call[:10]]
    (RUNTIME_DIR/"closer"/"daily_call_sheet.md").write_text("\n".join(c)+"\n",encoding="utf-8")
    with (RUNTIME_DIR/"closer"/"daily_call_sheet.csv").open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=["rank","lead_id","reality_status","city","trade","score","category","evidence_url"]); w.writeheader(); [w.writerow({"rank":i,"lead_id":l["id"],"reality_status":l["reality_status"],"city":l.get("city",""),"trade":l.get("trade_hint",""),"score":l["score_total"],"category":l["category"],"evidence_url":l.get("evidence_url","")}) for i,l in enumerate(callables[:15],1)]
    (RUNTIME_DIR/"closer"/"priority_leads.md").write_text("\n".join([f"- {l['id']} {l['score_total']}" for l in leads if l['category'] in {"TITAN","GROS"}]),encoding="utf-8")
    return {"status":"ok","total":len(leads),"counts":Counter([l["reality_status"] for l in leads]),"categories":Counter([l["category"] for l in leads])}

if __name__=="__main__":
    import sys
    m=sys.argv[1] if len(sys.argv)>1 else "run"
    s=run_pipeline(m)
    if m=="crm-summary":
        print("Mode CRM: atlas/runtime/crm/leads_history.json")
    else:
        print("ATLAS RAPPORTEUR D’AFFAIRES — V0.7")
        print("Status: OK")
        print(f"Leads traités: {s['total']}")
        print(f"Leads réels URL: {s['counts'].get('COLLECTED_FROM_URL',0)+s['counts'].get('PARTIALLY_VERIFIED',0)}")
        print(f"Leads manuels: {s['counts'].get('MANUAL',0)}")
        print(f"Leads démo: {s['counts'].get('DEMO',0)}")
        for k in ["TITAN","GROS","MOYEN","PETIT","FAIBLE"]: print(f"{k}: {s['categories'].get(k,0)}")
        print("Rapport:\natlas/runtime/reports/lead_report.md")
        print("Fiche closer:\natlas/runtime/closer/daily_call_sheet.md")
        print("Exports:\natlas/runtime/export/leads_ranked.json\natlas/runtime/export/leads_ranked.csv")
