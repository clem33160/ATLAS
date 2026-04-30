from __future__ import annotations

from .common import RUNTIME_PATHS, read_json, write_json


def build_active_context(task: str, domain: str | None = None) -> dict:
    return {
        "objectif_actuel": task,
        "domain": domain,
        "regles_importantes": [
            "append_only",
            "no_fake_proofs",
            "no_active_noise",
            "human_validation_for_canon",
            "one_domain_one_authority",
            "no_runtime_pollution",
            "no_destructive_delete",
            "provenance_required",
            "uncertainty_tracked",
            "conflicts_are_official_objects",
        ],
        "risques_immediats": ["canon_conflict", "privacy_violation"],
        "connaissances_pertinentes": ["raw", "semantic", "canon"],
        "etapes_en_cours": ["ingest", "extract", "audit"],
    }


def save_active_context(context: dict) -> None:
    write_json(RUNTIME_PATHS["active"], context)


def load_active_context() -> dict:
    return read_json(RUNTIME_PATHS["active"], {})
