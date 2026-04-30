from urllib.parse import urlparse
from datetime import datetime
from .models import Lead

TRADES = ['plomberie','chauffage','toiture','électricité','rénovation']

def extract_leads(results, pages):
    leads=[]
    for r in results:
        text = pages.get(r['url'], '')
        city = 'Lyon' if 'Lyon' in text else ('Bruxelles' if 'Bruxelles' in text else 'INCONNU')
        country = 'France' if city=='Lyon' else ('Belgique' if city=='Bruxelles' else 'INCONNU')
        trade = next((t for t in TRADES if t in (r['title']+' '+text).lower()), 'INCONNU')
        leads.append(Lead(title=r['title'],url=r['url'],snippet=r['snippet'],raw_text_excerpt=text[:280],city=city,country=country,trade=trade,urgency='URGENT' if 'urgent' in text.lower() else 'NORMAL',budget_visible='OUI' if 'budget' in text.lower() or 'EUR' in text else 'INCONNU',contact_public='OUI' if any(c.isdigit() for c in text) else 'INCONNU',source_domain=urlparse(r['url']).netloc,collected_at=datetime.utcnow().isoformat()))
    return leads
