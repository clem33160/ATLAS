from core.access.policies import POLICIES

def can_access(role: str, category: str, linked_client: str | None = None, actor_client: str | None = None) -> bool:
    allowed = POLICIES.get(role, set())
    if "*" in allowed:
        return True
    if role == "external_client":
        return category == "client_doc" and linked_client and actor_client and linked_client == actor_client
    return category in allowed
