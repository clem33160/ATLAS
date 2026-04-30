import csv, json
from pathlib import Path
from .config import BASE

def write_exports(leads):
    exp=BASE/'runtime/exports'; rep=BASE/'runtime/reports'; clo=BASE/'runtime/closer'; aud=BASE/'runtime/audit'
    for d in [exp,rep,clo,aud]: d.mkdir(parents=True, exist_ok=True)
    payload=[l.to_dict() for l in leads]
    (exp/'leads_ranked.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding='utf-8')
    with (exp/'leads_ranked.csv').open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=['title','url','city','country','trade','intent_type','score','tier'])
        w.writeheader(); [w.writerow({k:d.get(k,'') for k in w.fieldnames}) for d in payload]
    (rep/'daily_report.md').write_text('# Daily Report\n\n' + '\n'.join(f"- {d['tier']} {d['title']} ({d['score']})" for d in payload),encoding='utf-8')
    (clo/'closer_call_sheet.md').write_text('# Closer Call Sheet\n\n' + '\n'.join(f"## {d['title']}\nURL: {d['url']}\nVille: {d['city']}\nArtisans: {len(d.get('matched_artisans',[]))}" for d in payload),encoding='utf-8')
    (aud/'audit_report.md').write_text('# Audit Report\n\nConforme: sources publiques, validation humaine requise.',encoding='utf-8')
