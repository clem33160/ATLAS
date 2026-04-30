from dataclasses import dataclass, asdict, field
from typing import List

@dataclass
class Lead:
    title: str
    url: str
    snippet: str
    raw_text_excerpt: str = "ABSENT"
    city: str = "INCERTAIN"
    country: str = "INCERTAIN"
    trade: str = "INCERTAIN"
    urgency: str = "NORMAL"
    intent_type: str = "UNKNOWN"
    source_domain: str = "INCERTAIN"
    freshness_days: int = 3
    contact_public: str = "ABSENT"
    contact_phone: str = "ABSENT"
    contact_email: str = "ABSENT"
    contact_form: str = "ABSENT"
    score: int = 0
    tier: str = "REJETE"
    qualification_reasons: List[str] = field(default_factory=list)
    rejection_reasons: List[str] = field(default_factory=list)
    confidence: float = 0.0
    matched_artisans: List[dict] = field(default_factory=list)

    def to_dict(self):
        return asdict(self)
