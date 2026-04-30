from dataclasses import dataclass, asdict
from typing import List

VALID_INTENTS = {"CLIENT_REQUEST", "PUBLIC_MARKET", "ARTISAN_AD", "DIRECTORY_PAGE", "JOB_OFFER", "BLOG_ARTICLE", "TRAINING", "UNKNOWN"}

@dataclass
class Lead:
    title: str
    url: str
    snippet: str
    raw_text_excerpt: str = "INCONNU"
    city: str = "INCONNU"
    country: str = "INCONNU"
    trade: str = "INCONNU"
    urgency: str = "INCONNU"
    budget_visible: str = "INCONNU"
    contact_public: str = "INCONNU"
    source_domain: str = "INCONNU"
    collected_at: str = "INCONNU"
    intent_type: str = "UNKNOWN"
    score: int = 0
    tier: str = "ARCHIVE"
    matched_artisans: List[dict] = None

    def to_dict(self):
        d = asdict(self)
        d["matched_artisans"] = self.matched_artisans or []
        return d
