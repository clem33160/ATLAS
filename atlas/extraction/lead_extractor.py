from __future__ import annotations
from .patterns import URGENT_KEYWORDS, MARKET_KEYWORDS, DIRECTORY_KEYWORDS, AD_KEYWORDS, CLIENT_KEYWORDS
from .geography import detect_city_country_zip
from .trades import detect_trade
from .budget import detect_budget


def detect_intent_type(text:str)->str:
    t=(text or '').lower()
    if any(k in t for k in MARKET_KEYWORDS): return 'PUBLIC_MARKET'
    if any(k in t for k in DIRECTORY_KEYWORDS): return 'DIRECTORY_PAGE'
    if any(k in t for k in AD_KEYWORDS): return 'ARTISAN_AD'
    if any(k in t for k in CLIENT_KEYWORDS): return 'CLIENT_REQUEST'
    if len(t)<80: return 'GENERIC_PAGE'
    return 'UNKNOWN'


def extract_signals(text: str) -> dict:
    geo=detect_city_country_zip(text)
    tr=detect_trade(text)
    bd=detect_budget(text)
    t=(text or '').lower()
    urgency='high' if any(k in t for k in URGENT_KEYWORDS) else 'medium'
    return {**geo, **tr, **bd, 'urgency':urgency, 'intent_type':detect_intent_type(text)}
