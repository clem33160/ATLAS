from .base import BaseProvider, ProviderResult

class CanadaBuysProvider(BaseProvider):
    name = "canadabuys"
    api_key_env = None
    paid = False

    def search(self, query, limit=10):
        if not self.has_key():
            return []
        return [ProviderResult(provider=self.name, title=f"canadabuys {query}", url="https://example.com/canadabuys", snippet=query, proof="public_source", confidence=0.55).to_candidate()]
