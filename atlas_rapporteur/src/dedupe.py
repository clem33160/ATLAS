import hashlib
from urllib.parse import urlparse

def dedupe_leads(leads):
    seen=set(); out=[]
    for l in leads:
        dom=urlparse(l.url).netloc
        text_hash=hashlib.sha1((l.title.lower()+l.snippet.lower()).encode()).hexdigest()[:12]
        k=(l.url.lower(),dom,text_hash,l.contact_phone,l.contact_email,l.city.lower(),l.trade.lower())
        if k in seen:
            continue
        seen.add(k); out.append(l)
    return out
