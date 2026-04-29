from __future__ import annotations
from .patterns import TRADES

def detect_trade(text:str)->dict:
    t=(text or '').lower()
    for family, words in TRADES.items():
        if any(w in t for w in words):
            return {'trade':words[0], 'trade_family':family}
    return {'trade':'', 'trade_family':''}
