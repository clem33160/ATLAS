def dedupe_leads(leads):
    seen=set(); out=[]
    for l in leads:
        key=(l.url.strip().lower(), l.title.strip().lower(), l.city.lower(), l.trade.lower())
        if key in seen: continue
        seen.add(key); out.append(l)
    return out
