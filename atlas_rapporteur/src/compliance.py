def is_potential_lead(lead):
    if lead.intent_type not in ('CLIENT_REQUEST','PUBLIC_MARKET'):
        return False
    if lead.city=='INCONNU' or lead.trade=='INCONNU':
        return False
    if len((lead.raw_text_excerpt or '')) < 30:
        return False
    return True
