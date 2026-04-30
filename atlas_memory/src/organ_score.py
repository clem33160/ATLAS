from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .common import RUNTIME_PATHS, ensure_runtime_structure, read_json, read_jsonl, write_json
from .health import compute_health


@dataclass(frozen=True)
class LayerSpec:
    key: str
    label: str
    source_patterns: tuple[str, ...]
    test_patterns: tuple[str, ...]
    runtime_keys: tuple[str, ...]


LAYER_SPECS: tuple[LayerSpec, ...] = (
    LayerSpec("raw", "mémoire brute", ("atlas_memory/src/raw_store.py",), ("atlas_memory/tests/test_raw_append_only.py",), ("raw",)),
    LayerSpec("semantic", "mémoire sémantique", ("atlas_memory/src/semantic_store.py",), ("atlas_memory/tests/test_semantic_extraction.py",), ("semantic",)),
    LayerSpec("canon", "mémoire canonique", ("atlas_memory/src/canon_store.py",), ("atlas_memory/tests/test_canon_promotion.py",), ("canon",)),
    LayerSpec("causal", "mémoire causale", ("atlas_memory/src/semantic_store.py",), (), ("causal",)),
    LayerSpec("procedural", "mémoire procédurale", ("atlas_memory/src/procedure_store.py",), ("atlas_memory/tests/test_memory.py",), ("procedures",)),
    LayerSpec("self", "mémoire de soi", ("atlas_memory/src/self_memory.py",), ("atlas_memory/tests/test_memory.py",), ("self",)),
    LayerSpec("objectives", "mémoire des objectifs", ("atlas_memory/src/objective_store.py",), ("atlas_memory/tests/test_memory.py",), ("objectives",)),
    LayerSpec("uncertainty", "mémoire d’incertitude", ("atlas_memory/src/uncertainty_store.py",), ("atlas_memory/tests/test_uncertainty.py",), ("uncertainty",)),
    LayerSpec("contradictions", "mémoire des contradictions", ("atlas_memory/src/conflict_store.py",), ("atlas_memory/tests/test_conflict_detection.py",), ("conflict",)),
    LayerSpec("temporal", "mémoire temporelle", ("atlas_memory/src/temporal_store.py",), ("atlas_memory/tests/test_temporal_timeline.py",), ("temporal",)),
    LayerSpec("simulation", "mémoire de simulation", ("atlas_memory/src/simulation_store.py",), (), ("simulation",)),
    LayerSpec("social", "mémoire sociale", ("atlas_memory/src/self_memory.py",), (), ("social",)),
    LayerSpec("audit", "mémoire d’audit", ("atlas_memory/src/audit_ledger.py",), ("atlas_memory/tests/test_health.py",), ("audit",)),
    LayerSpec("hierarchical", "mémoire hiérarchique", ("atlas_memory/src/global_index.py",), ("atlas_memory/tests/test_global_index.py",), ("index",)),
    LayerSpec("active", "mémoire active", ("atlas_memory/src/active_context.py",), ("atlas_memory/tests/test_active_context.py",), ("active",)),
    LayerSpec("self_organizing", "mémoire auto-organisatrice", ("atlas_memory/src/organizer.py",), (), ("index", "active")),
    LayerSpec("anti_forgetting", "mémoire anti-oubli", ("atlas_memory/src/anti_forgetting.py",), ("atlas_memory/tests/test_anti_forgetting.py",), ("audit", "objectives")),
    LayerSpec("anti_noise", "mémoire anti-bruit", ("atlas_memory/src/noise_guard.py", "atlas_memory/src/noise_quarantine.py"), ("atlas_memory/tests/test_noise_guard_quarantine.py",), ("raw",)),
    LayerSpec("value", "mémoire de valeur", ("atlas_memory/src/value_store.py",), (), ("audit",)),
    LayerSpec("governed", "mémoire gouvernée", ("atlas_memory/src/governance.py",), ("atlas_memory/tests/test_doctrine_check.py",), ("audit", "index")),
)


def _has_pattern(patterns: tuple[str, ...]) -> bool:
    return all(Path(p).exists() for p in patterns)


def _runtime_presence(keys: tuple[str, ...]) -> tuple[bool, list[str]]:
    proofs: list[str] = []
    ok = True
    for key in keys:
        path = RUNTIME_PATHS[key]
        exists = path.exists()
        if not exists:
            nonempty = False
        elif path.is_dir():
            nonempty = any(path.iterdir())
        elif path.suffix == ".jsonl":
            nonempty = len(read_jsonl(path)) > 0
        else:
            nonempty = bool(read_json(path, {}))
        state = "OK" if nonempty else ("EMPTY" if exists else "MISSING")
        proofs.append(f"runtime:{key}:{state}")
        ok = ok and nonempty
    return ok, proofs


def _integration_refs() -> dict[str, bool]:
    rapporteur_hits = [
        "atlas_rapporteur/src/main.py",
        "atlas_rapporteur/src/reports.py",
        "atlas_memory/tests/test_integration_rapporteur.py",
    ]
    governance_hits = [
        "atlas_governance/core/authority_index.py",
        "atlas_governance/core/domain_registry.py",
        "atlas_memory/src/governance.py",
    ]
    return {
        "rapporteur": any(Path(p).exists() for p in rapporteur_hits),
        "governance": any(Path(p).exists() for p in governance_hits),
    }


def compute_organ_score() -> dict[str, Any]:
    ensure_runtime_structure()
    health = compute_health()
    integration = _integration_refs()

    layer_scores: dict[str, Any] = {}
    missing_caps: list[str] = []
    gaps: list[dict[str, Any]] = []

    for layer in LAYER_SPECS:
        score = 0
        proofs: list[str] = []
        limits: list[str] = []

        if _has_pattern(layer.source_patterns):
            score += 15
            proofs.append("source:present")
        else:
            limits.append("code source incomplet")

        if layer.test_patterns and _has_pattern(layer.test_patterns):
            score += 15
            proofs.append("tests:present")
        else:
            limits.append("tests absents/partiels")

        runtime_ok, runtime_proofs = _runtime_presence(layer.runtime_keys)
        proofs.extend(runtime_proofs)
        if runtime_ok:
            score += 20
        else:
            limits.append("preuve runtime insuffisante")

        if Path(RUNTIME_PATHS["index"]).exists():
            score += 10
            proofs.append("global_index:present")
        else:
            limits.append("non indexée globalement")

        if Path(RUNTIME_PATHS["active"]).exists():
            score += 10
            proofs.append("active_context:present")

        if health.get("active_pollution_found") is False:
            score += 5
            proofs.append("anti_pollution:ok")

        if health.get("audit_events_count", 0) > 0:
            score += 10
            proofs.append("audit:present")

        if integration["rapporteur"]:
            score += 7
            proofs.append("rapporteur:visible")
        else:
            limits.append("intégration rapporteur faible")

        if integration["governance"]:
            score += 8
            proofs.append("governance:visible")
        else:
            limits.append("intégration governance faible")

        score = min(score, 100)
        status = "solide" if score >= 80 else "partielle" if score >= 55 else "squelette"
        layer_scores[layer.key] = {"label": layer.label, "score": score, "status": status, "proofs": proofs, "remaining_limits": limits}
        if score < 75:
            missing_caps.append(layer.label)
            gaps.append({"layer": layer.label, "score": score, "main_gap": limits[0] if limits else "couverture incomplète"})

    base_global_score = round(sum(x["score"] for x in layer_scores.values()) / len(layer_scores), 2)
    integration_score = 62 if integration["rapporteur"] and integration["governance"] else 45

    critical_missing = {"mémoire causale", "mémoire de simulation", "mémoire sociale"}
    if critical_missing.intersection(missing_caps):
        global_score = min(base_global_score, 70.0)
    else:
        global_score = base_global_score

    ordered_gaps = sorted(gaps, key=lambda g: g["score"])[:10]
    verdict = "PAS PRÊT V2 profonde" if global_score < 75 else "PRÊT sous conditions"
    priorities = [
        "Activer une mémoire causale exploitable avec tests dédiés.",
        "Connecter la simulation à des preuves runtime non vides.",
        "Ajouter mémoire sociale active et consommation par rapporteur.",
        "Renforcer l’usage atlas_governance + atlas_rapporteur en production.",
        "Prouver l’orchestration par couches via audit granulaire.",
    ]

    report = {
        "global_organ_score": global_score,
        "technical_health_score": health.get("memory_score", 0),
        "integration_score": integration_score,
        "layer_scores": layer_scores,
        "missing_capabilities": missing_caps,
        "top_10_gaps": ordered_gaps,
        "next_v2_priorities": priorities,
        "false_positive_risks": [
            "Score santé 100 peut masquer des couches runtime vides.",
            "Présence de fichiers ne garantit pas exploitation réelle.",
            "Intégration visible sans flux bidirectionnel complet.",
        ],
        "verdict": verdict,
    }

    json_path = RUNTIME_PATHS["health_json"].parent / "memory_organ_score.json"
    md_path = RUNTIME_PATHS["health_md"].parent / "memory_organ_score.md"
    write_json(json_path, report)

    solid = [v["label"] for v in layer_scores.values() if v["status"] == "solide"]
    partial = [v["label"] for v in layer_scores.values() if v["status"] == "partielle"]
    skeleton = [v["label"] for v in layer_scores.values() if v["status"] == "squelette"]
    md = [
        "# Memory Organ Score",
        f"- global_organ_score: {global_score}",
        f"- technical_health_score: {health.get('memory_score', 0)}",
        f"- integration_score: {integration_score}",
        f"- verdict: {verdict}",
        "",
        "## Pourquoi ce n'est pas 100%",
        "- Le score organique exige preuves runtime par couche et intégration profonde, pas seulement santé technique.",
        "",
        "## Couches solides",
        *(f"- {x}" for x in solid),
        "",
        "## Couches partielles",
        *(f"- {x}" for x in partial),
        "",
        "## Couches squelettes",
        *(f"- {x}" for x in skeleton),
        "",
        "## Objectifs progressifs",
        "- 75%: causalité + simulation + sociale avec runtime non vide.",
        "- 85%: intégration rapporteur/gouvernance bidirectionnelle prouvée.",
        "- 95%: audits couche-par-couche et réduction des limites restantes.",
    ]
    md_path.write_text("\n".join(md) + "\n", encoding="utf-8")
    return report
