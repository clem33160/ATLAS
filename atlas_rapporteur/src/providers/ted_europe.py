from .base import BaseProvider, ProviderResult

class TedEuropeProvider(BaseProvider):
    name = "ted"
    api_key_env = None
    paid = False

    def search(self, query, limit=10):
        if not self.has_key():
            return []
        return [ProviderResult(provider=self.name, title=f"ted {query}", url="https://example.com/ted", snippet=query, proof="public_source", confidence=0.55).to_candidate()]
