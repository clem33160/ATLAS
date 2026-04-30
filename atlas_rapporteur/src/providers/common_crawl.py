from .base import BaseProvider, ProviderResult

class CommonCrawlProvider(BaseProvider):
    name = "common_crawl"
    api_key_env = None
    paid = False

    def search(self, query, limit=10):
        if not self.has_key():
            return []
        return [ProviderResult(provider=self.name, title=f"common_crawl {query}", url="https://example.com/common_crawl", snippet=query, proof="public_source", confidence=0.55).to_candidate()]
