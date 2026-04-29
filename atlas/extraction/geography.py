from __future__ import annotations
import re
from .patterns import FR_CITIES

def detect_city_country_zip(text: str) -> dict:
    t=(text or '').lower()
    city=''
    for c in FR_CITIES:
        if c in t:
            city=c.title(); break
    zip_m=re.search(r'\b(\d{5})\b', t)
    country='FR' if city or zip_m else ''
    return {'city':city,'zip_code':zip_m.group(1) if zip_m else '','country':country}
