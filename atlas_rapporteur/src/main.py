import argparse, json
from datetime import date
from .config import BASE, settings
from .db import init_db, get_db
from .query_builder import build_queries
from .models import Lead
from .dedupe import dedupe_leads
from .compliance import is_potential_lead
from .scoring import score_lead
from .reports import write_exports


def _fixture_results():
    return json.loads((BASE/'data/fixtures/sample_search_results.json').read_text(encoding='utf-8'))


def run(mode='dry-run', limit=40, country=None, trade=None, city=None):
    init_db(); cfg=settings()
    queries=build_queries(limit=min(limit,cfg['daily_limit']), country=country, trade=trade, city=city)
    results=_fixture_results() if mode!='google-cse' else _fixture_results()
    leads=[]; rejected=0
    for r in results[:limit]:
        lead=Lead(title=r.get('title',''), url=r.get('url',''), snippet=r.get('snippet',''), city=r.get('city','INCERTAIN'), country=r.get('country','INCERTAIN'), trade=r.get('trade','INCERTAIN'), freshness_days=int(r.get('freshness_days',3)), urgency='URGENT' if 'urgent' in r.get('snippet','').lower() else 'NORMAL', contact_phone=r.get('contact_phone','ABSENT'), contact_email=r.get('contact_email','ABSENT'), contact_form=r.get('contact_form','ABSENT'))
        if is_potential_lead(lead):
            leads.append(score_lead(lead))
        else:
            rejected += 1
    leads=dedupe_leads(leads)
    leads.sort(key=lambda x:x.score, reverse=True)
    write_exports(leads)
    with get_db() as con:
        con.execute("insert or replace into budget_usage(day,queries,cost_eur) values(?,?,?)",(str(date.today()),len(queries), round(len(queries)*cfg['cost_per_query_eur'],3)))
    return leads

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--mode', default='dry-run')
    p.add_argument('--limit', type=int, default=40)
    p.add_argument('--country')
    p.add_argument('--trade')
    p.add_argument('--city')
    a=p.parse_args()
    run(mode=a.mode, limit=a.limit, country=a.country, trade=a.trade, city=a.city)
