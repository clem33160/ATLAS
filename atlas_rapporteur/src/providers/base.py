from dataclasses import dataclass
from datetime import datetime

@dataclass
class ProviderResult:
    provider: str
    title: str
    url: str
    snippet: str
    country: str = "INCONNU"
    city: str = "INCONNU"
    trade: str = "INCONNU"
    proof: str = "ABSENT"
    confidence: float = 0.0
    collected_at: str = ""

    def to_candidate(self):
        return {"provider": self.provider, "title": self.title or "ABSENT", "url": self.url or "ABSENT", "snippet": self.snippet or "ABSENT", "country": self.country or "INCONNU", "city": self.city or "INCONNU", "trade": self.trade or "INCONNU", "proof": self.proof or "ABSENT", "confidence": float(self.confidence), "collected_at": self.collected_at or datetime.utcnow().isoformat()}

class BaseProvider:
    name = "base"
    api_key_env = None
    paid = False
    def has_key(self):
        if not self.api_key_env:
            return True
        import os
        return bool(os.getenv(self.api_key_env))
    def search(self, query, limit=10):
        raise NotImplementedError
