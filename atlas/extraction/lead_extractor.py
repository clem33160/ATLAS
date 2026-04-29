from __future__ import annotations
import re
from .patterns import TRADES, URGENT_KEYWORDS


def extract_signals(text: str) -> dict:
    t = (text or "").lower()
    trade = next((x for x in TRADES if x in t), "")
    urgency = "high" if any(k in t for k in URGENT_KEYWORDS) else "medium"
    budget_m = re.findall(r"(\d{2,6})\s*€", t)
    city = ""
    for c in ["lyon", "marseille", "toulouse", "paris"]:
        if c in t:
            city = c.title()
            break
    zip_match = re.search(r"\b(\d{5})\b", t)
    return {
        "city": city,
        "zip_code": zip_match.group(1) if zip_match else "",
        "trade_hint": trade,
        "budget_eur": int(budget_m[0]) if budget_m else 0,
        "budget_confidence": "EXACT" if budget_m else "FAIBLE",
        "urgency": urgency,
        "keywords": [k for k in URGENT_KEYWORDS if k in t],
        "incertitudes": ["ville inconnue"] if not city else [],
    }
