from .config import load_json

def score_lead(lead):
    w=load_json('config/scoring.json')['weights']
    s=0
    s += w['valeur_chantier'] if lead.intent_type in ('PUBLIC_MARKET','CLIENT_REQUEST') else 0
    s += w['urgence'] if lead.urgency=='URGENT' else 5
    s += 10
    s += w['clarte'] if lead.city!='INCONNU' and lead.trade!='INCONNU' else 2
    s += w['preuve_source'] if lead.source_domain!='INCONNU' else 0
    s += w['domaine_rentable'] if lead.trade!='INCONNU' else 0
    s += w['localisation'] if lead.city!='INCONNU' else 0
    s += w['facilite_artisan'] if lead.contact_public=='OUI' else 0
    s += 3
    lead.score=min(100,s)
    t=load_json('config/scoring.json')['tiers']
    lead.tier='TITAN' if lead.score>=t['TITAN'] else 'GROS' if lead.score>=t['GROS'] else 'MOYEN' if lead.score>=t['MOYEN'] else 'PETIT' if lead.score>=t['PETIT'] else 'ARCHIVE'
    return lead
