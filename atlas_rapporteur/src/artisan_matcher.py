import csv
from .config import BASE

def match_artisans(lead, max_n=5):
    rows=[]
    with (BASE/'inbox/manual_artisans.csv').open(encoding='utf-8') as f:
        for r in csv.DictReader(f):
            if r['trade']!=lead.trade: continue
            if r['country']!=lead.country and lead.country!='INCONNU': continue
            score=2 + (2 if r['city']==lead.city else 0) + (1 if r.get('phone') else 0)
            if not r.get('source'): continue
            rows.append((score,r))
    rows.sort(reverse=True,key=lambda x:x[0])
    lead.matched_artisans=[r for _,r in rows[:max_n]]
    return lead
