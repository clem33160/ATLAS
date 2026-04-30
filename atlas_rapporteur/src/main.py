import argparse, json
from .query_builder import build_queries
from .search_google_cse import search_google_cse, google_cse_available
from .search_manual import search_manual
from .fetcher import fetch_pages
from .extractor import extract_leads
from .analyzer_heuristic import analyze_heuristic
from .analyzer_openai import openai_available, analyze_openai_stub
from .dedupe import dedupe_leads
from .scoring import score_lead
from .artisan_matcher import match_artisans
from .compliance import is_potential_lead
from .reports import write_exports
from .db import init_db
from .config import BASE

def run(mode='dry-run', limit=20):
    init_db()
    queries=build_queries(limit=limit)
    if mode=='google-cse' and google_cse_available():
        results=search_google_cse(queries, limit=limit)
    elif mode=='manual':
        results=search_manual()
    else:
        results=json.loads((BASE/'data/fixtures/sample_search_results.json').read_text(encoding='utf-8'))
    pages=fetch_pages(results, dry_run=(mode!='google-cse'))
    leads=dedupe_leads(extract_leads(results,pages))
    processed=[]
    for l in leads:
        l=analyze_heuristic(l)
        if openai_available():
            _=analyze_openai_stub(l)
        if not is_potential_lead(l):
            continue
        l=score_lead(l)
        l=match_artisans(l)
        processed.append(l)
    processed.sort(key=lambda x:x.score, reverse=True)
    write_exports(processed)
    return processed

if __name__ == '__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--dry-run', action='store_true')
    p.add_argument('--manual', action='store_true')
    p.add_argument('--google-cse', action='store_true')
    p.add_argument('--limit', type=int, default=20)
    a=p.parse_args()
    mode='google-cse' if a.google_cse else 'manual' if a.manual else 'dry-run'
    run(mode=mode, limit=a.limit)
