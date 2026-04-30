from __future__ import annotations

from .common import RUNTIME_PATHS, read_json, write_json


def record_social_signal(signal_type: str, actor: str, detail: str, consent_explicit: bool) -> dict | None:
    if not consent_explicit:
        return None
    state = read_json(RUNTIME_PATHS["social"], {})
    history = state.get("history", [])
    history.append({
        "signal_type": signal_type,
        "actor": actor,
        "detail": detail,
        "consent_explicit": True,
    })
    state["history"] = history
    state["last_signal"] = history[-1]
    write_json(RUNTIME_PATHS["social"], state)
    return state["last_signal"]


def list_social_signals() -> list[dict]:
    return read_json(RUNTIME_PATHS["social"], {}).get("history", [])
