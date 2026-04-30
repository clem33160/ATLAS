from __future__ import annotations

import os
from pathlib import Path
from .common import get_runtime_dir, write_json

REQUIRED_KEYS = ("OPENAI_API_KEY", "TAVILY_API_KEY")


def run_production_check(mode: str = "dry-run") -> dict:
    keys = {k: bool(os.getenv(k, "").strip()) for k in REQUIRED_KEYS}
    fixtures_used = Path("atlas_rapporteur/data/fixtures/sample_search_results.json").exists()
    if mode == "production":
        ok = all(keys.values())
        reason = "missing_api_keys" if not ok else "ready"
    else:
        ok = True
        reason = "dry_run_safe"

    out = {
        "mode": mode,
        "required_keys": keys,
        "fixtures_available": fixtures_used,
        "automatic_external_contact": False,
        "ok": ok,
        "reason": reason,
    }
    write_json(get_runtime_dir() / "reports" / "production_readiness.json", out)
    return out
