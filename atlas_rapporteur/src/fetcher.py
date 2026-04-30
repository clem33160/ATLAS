from urllib.parse import urlparse
from .config import load_json, BASE
import json

def fetch_pages(results, dry_run=True):
    policy = load_json('config/source_policy.json')
    fixture = json.loads((BASE/'data/fixtures/sample_pages.json').read_text(encoding='utf-8'))
    pages = {}
    for r in results:
        u = r['url']
        d = urlparse(u).netloc
        if any(x in d for x in policy['blocked_domains_contains']):
            continue
        pages[u] = fixture.get(u, r.get('snippet','INCONNU')) if dry_run else r.get('snippet','INCONNU')
    return pages
