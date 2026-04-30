from .base import BaseProvider, ProviderResult

class SeaoQuebecProvider(BaseProvider):
    name = "seao"
    api_key_env = None
    paid = False

    def search(self, query, limit=10):
        if not self.has_key():
            return []
        return [ProviderResult(provider=self.name, title=f"seao {query}", url="https://example.com/seao", snippet=query, proof="public_source", confidence=0.55).to_candidate()]
