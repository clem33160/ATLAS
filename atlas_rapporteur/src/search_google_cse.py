import json, urllib.parse, urllib.request
from .config import env

def google_cse_available():
    return bool(env('GOOGLE_CSE_API_KEY')) and bool(env('GOOGLE_CSE_CX'))

def search_google_cse(queries, limit=20):
    key, cx = env('GOOGLE_CSE_API_KEY'), env('GOOGLE_CSE_CX')
    items = []
    for q in queries[:max(1, min(limit, 10))]:
        url = f"https://www.googleapis.com/customsearch/v1?{urllib.parse.urlencode({'key': key, 'cx': cx, 'q': q})}"
        with urllib.request.urlopen(url, timeout=10) as r:
            payload = json.loads(r.read().decode('utf-8'))
        for it in payload.get('items', []):
            items.append({'title': it.get('title','INCONNU'), 'url': it.get('link','INCONNU'), 'snippet': it.get('snippet','INCONNU')})
    return items[:limit]
