import csv, json
from .config import BASE

def write_exports(leads):
    exp=BASE/'runtime/exports'; rep=BASE/'runtime/reports'
    exp.mkdir(parents=True, exist_ok=True); rep.mkdir(parents=True, exist_ok=True)
    payload=[l.to_dict() for l in leads]
    (exp/'leads_ranked.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding='utf-8')
    with (exp/'leads_ranked.csv').open('w',encoding='utf-8',newline='') as f:
        fields=['title','url','city','country','trade','contact_phone','contact_email','score','tier']
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader()
        for d in payload: w.writerow({k:d.get(k,'') for k in fields})
    lines=['# Rapport quotidien Atlas','','|Score|Catégorie|Métier|Ville|URL|','|---:|---|---|---|---|']
    for d in payload[:50]: lines.append(f"|{d['score']}|{d['tier']}|{d['trade']}|{d['city']}|{d['url']}|")
    (rep/'daily_report.md').write_text('\n'.join(lines),encoding='utf-8')
