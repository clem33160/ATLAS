import os
import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]


def load_json(rel: str):
    return json.loads((BASE / rel).read_text(encoding="utf-8"))


def env(name: str, default=None):
    return os.getenv(name, default)


def settings():
    return {
        "search_provider": env("SEARCH_PROVIDER", "google_cse"),
        "google_key": env("GOOGLE_SEARCH_API_KEY") or env("GOOGLE_CSE_API_KEY", ""),
        "google_cx": env("GOOGLE_SEARCH_ENGINE_ID") or env("GOOGLE_CSE_CX", ""),
        "monthly_budget_eur": float(env("SEARCH_MONTHLY_BUDGET_EUR", "150")),
        "daily_limit": int(env("SEARCH_DAILY_LIMIT", "80")),
        "cost_per_query_eur": float(env("SEARCH_COST_PER_QUERY_EUR", "0.005")),
        "max_age_days": int(env("SEARCH_MAX_AGE_DAYS", "15")),
    }
