from .models import VALID_INTENTS

def analyze_heuristic(lead):
    t=(lead.title+' '+lead.snippet+' '+lead.raw_text_excerpt).lower()
    if 'blog' in t or 'article' in t: intent='BLOG_ARTICLE'
    elif 'emploi' in t or 'recrute' in t: intent='JOB_OFFER'
    elif 'annuaire' in t: intent='DIRECTORY_PAGE'
    elif 'formation' in t: intent='TRAINING'
    elif 'marché public' in t or 'appel d’offres' in t or 'avis de marché' in t: intent='PUBLIC_MARKET'
    elif 'cherche' in t or 'besoin' in t or 'devis' in t: intent='CLIENT_REQUEST'
    elif 'artisan' in t and 'services' in t: intent='ARTISAN_AD'
    else: intent='UNKNOWN'
    lead.intent_type = intent if intent in VALID_INTENTS else 'UNKNOWN'
    return lead
