from __future__ import annotations

from .common import RUNTIME_PATHS, has_sensitive_data, read_json, write_json


def init_self_memory() -> dict:
    state = {
        "system_name": "ATLAS",
        "mission": "Construire une infrastructure d'intelligence universelle gouvernée.",
        "limits": ["human_supervised", "no_illegal_actions"],
        "invariants": [
            "Atlas n’est pas un simple chatbot.", "Atlas doit éviter les fichiers ambigus.", "Atlas doit préserver les données.",
            "Atlas doit fonctionner avec gouvernance.", "Atlas doit rester humain-supervisé.", "Atlas ne doit pas inventer de preuves.",
            "Atlas ne doit pas agir illégalement.", "Atlas doit apprendre de ses erreurs."
        ],
        "current_active_modules": ["atlas_memory"],
        "forbidden_behaviors": ["fabrication_of_evidence", "chaotic_memory"]
    }
    write_json(RUNTIME_PATHS["self"], state)
    return state


def add_user_preference(key: str, value: str, consent: bool = True) -> dict:
    if not consent or has_sensitive_data({"key": key, "value": value}):
        raise ValueError("consent required and sensitive data forbidden")
    prefs = read_json(RUNTIME_PATHS["social"], {})
    prefs[key] = value
    write_json(RUNTIME_PATHS["social"], prefs)
    return prefs


def list_user_preferences() -> dict:
    return read_json(RUNTIME_PATHS["social"], {})
