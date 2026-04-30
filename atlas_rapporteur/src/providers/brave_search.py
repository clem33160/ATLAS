import json
import urllib.parse
import urllib.request
from urllib.error import HTTPError, URLError

from .base import BaseProvider, ProviderResult


class BraveSearchProvider(BaseProvider):
    name = "brave"
    api_key_env = "BRAVE_SEARCH_API_KEY"
    paid = True

    def search(self, query, limit=10):
        if not self.has_key():
            return []
        import os
        key = os.getenv(self.api_key_env, "")
        params = urllib.parse.urlencode({"q": query, "count": max(1, min(limit, 20))})
        req = urllib.request.Request(
            f"https://api.search.brave.com/res/v1/web/search?{params}",
            headers={"Accept": "application/json", "X-Subscription-Token": key},
            method="GET",
        )
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                payload = json.loads(resp.read().decode("utf-8"))
        except (HTTPError, URLError, TimeoutError):
            return []

        out = []
        for row in payload.get("web", {}).get("results", [])[:limit]:
            url = row.get("url", "")
            if not url or "example.com" in url:
                continue
            out.append(
                ProviderResult(
                    provider=self.name,
                    title=row.get("title", "ABSENT"),
                    url=url,
                    snippet=row.get("description", "ABSENT"),
                    proof="brave_web_search",
                    confidence=0.7,
                ).to_candidate()
            )
        return out
