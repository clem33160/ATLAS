from .base import BaseProvider


class BoampProvider(BaseProvider):
    name = "boamp"
    api_key_env = None
    paid = False

    def search(self, query, limit=10):
        return []
