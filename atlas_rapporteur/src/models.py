from dataclasses import dataclass, asdict, field
from datetime import datetime
from typing import List


@dataclass
class Lead:
    lead_id: str = "ABSENT"
    title: str = "ABSENT"
    source_url: str = "ABSENT"
    source_domain: str = "ABSENT"
    country: str = "INCONNU"
    city: str = "INCONNU"
    trade: str = "INCONNU"
    intent_type: str = "INCONNU"
    urgency: str = "NORMAL"
    freshness_days: int = 3
    budget_low: str = "ABSENT"
    budget_mid: str = "ABSENT"
    budget_high: str = "ABSENT"
    budget_status: str = "INCONNU"
    contact_public: str = "ABSENT"
    contact_phone: str = "ABSENT"
    contact_email: str = "ABSENT"
    contact_form: str = "ABSENT"
    evidence_summary: str = "ABSENT"
    raw_snippet: str = "ABSENT"
    raw_text_excerpt: str = "ABSENT"
    score: int = 0
    tier: str = "REJET"
    qualification_status: str = "TO_VALIDATE"
    rejection_reasons: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    matched_artisans: List[dict] = field(default_factory=list)
    url: str = "ABSENT"
    snippet: str = "ABSENT"

    def __post_init__(self):
        if self.source_url == "ABSENT" and self.url != "ABSENT": self.source_url = self.url
        if self.url == "ABSENT" and self.source_url != "ABSENT": self.url = self.source_url
        if self.raw_snippet == "ABSENT" and self.snippet != "ABSENT": self.raw_snippet = self.snippet
        if self.snippet == "ABSENT" and self.raw_snippet != "ABSENT": self.snippet = self.raw_snippet
        if self.raw_text_excerpt == "ABSENT" and self.raw_snippet != "ABSENT": self.raw_text_excerpt = self.raw_snippet

    def to_dict(self):
        return asdict(self)
