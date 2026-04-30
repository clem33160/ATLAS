from .config import load_json

def build_queries(limit=50):
    qp = load_json('config/query_packs.json')
    out = []
    for region, cities in qp['regions'].items():
        for city in cities:
            for trade in qp['trades'][:5]:
                for p in qp['patterns'][:3]:
                    out.append(p.format(trade=trade, city=city, country=region))
                    if len(out) >= limit:
                        return out
    return out
