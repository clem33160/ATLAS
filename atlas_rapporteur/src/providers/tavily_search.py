import json
import urllib.request
from urllib.error import HTTPError, URLError

from .base import BaseProvider, ProviderResult


class TavilySearchProvider(BaseProvider):
    name = "tavily"
    api_key_env = "TAVILY_API_KEY"
    paid = True

    def search(self, query, limit=10):
        if not self.has_key():
            return []
        import os
        key = os.getenv(self.api_key_env, "")
        body = json.dumps({"api_key": key, "query": query, "max_results": max(1, min(limit, 20))}).encode("utf-8")
        req = urllib.request.Request(
            "https://api.tavily.com/search",
            data=body,
            headers={"Content-Type": "application/json", "Accept": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                payload = json.loads(resp.read().decode("utf-8"))
        except (HTTPError, URLError, TimeoutError):
            return []

        out = []
        for row in payload.get("results", [])[:limit]:
            url = row.get("url", "")
            if not url or "example.com" in url:
                continue
            snippet = row.get("content") or row.get("snippet") or "ABSENT"
            out.append(
                ProviderResult(
                    provider=self.name,
                    title=row.get("title", "ABSENT"),
                    url=url,
                    snippet=snippet,
                    proof="tavily_search",
                    confidence=0.7,
                ).to_candidate()
            )
        return out
