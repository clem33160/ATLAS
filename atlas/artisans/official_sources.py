from pathlib import Path

def load_official_urls(path: Path):
    if not path.exists(): return []
    out=[]
    for l in path.read_text(encoding='utf-8').splitlines():
        l=l.strip()
        if l and not l.startswith('#'): out.append({'source_url':l})
    return out
