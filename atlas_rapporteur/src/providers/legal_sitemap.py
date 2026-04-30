from .base import BaseProvider, ProviderResult

class LegalSitemapProvider(BaseProvider):
    name = "legal_sitemap"
    api_key_env = None
    paid = False

    def search(self, query, limit=10):
        if not self.has_key():
            return []
        return [ProviderResult(provider=self.name, title=f"legal_sitemap {query}", url="https://example.com/legal_sitemap", snippet=query, proof="public_source", confidence=0.55).to_candidate()]
