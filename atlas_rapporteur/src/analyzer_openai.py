import json
from .config import env

def openai_available():
    return bool(env('OPENAI_API_KEY'))

def analyze_openai_stub(lead):
    # JSON structuré strict (mock local sans dépendance)
    return {
      "is_real_opportunity": lead.intent_type in ("CLIENT_REQUEST", "PUBLIC_MARKET"),
      "intent_type": lead.intent_type,
      "trade": lead.trade,
      "city": lead.city,
      "country": lead.country,
      "urgency": lead.urgency,
      "budget_estimate_low": 0,
      "budget_estimate_mid": 0,
      "budget_estimate_high": 0,
      "evidence_summary": lead.raw_text_excerpt[:120],
      "risk_flags": [],
      "missing_fields": [k for k,v in {"city":lead.city,"trade":lead.trade}.items() if v=="INCONNU"],
      "recommended_action": "HUMAN_REVIEW",
      "confidence": 0.6
    }
