from __future__ import annotations

import json
from typing import Any

SYNTHETIC_TOKENS = {
    "demo", "test", "tests", "fixture", "mock", "synthetic", "exemple", "example", "sandbox", "tmp", "generated_test", "cmd_demo",
}
PLACEHOLDER_TOKENS = {"lorem", "todo", "placeholder", "example.com"}


def _flat_text(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False).lower() if isinstance(value, (dict, list)) else str(value).lower()


def is_synthetic_source(value: Any) -> bool:
    text = _flat_text(value)
    return any(token in text for token in SYNTHETIC_TOKENS)


def is_placeholder_claim(item: dict[str, Any]) -> bool:
    pairs = {
        "claim": "claim",
        "claim_a": "x",
        "claim_b": "y",
        "missing_evidence": "proof",
        "reason": "reason",
        "source_a": "a",
        "source_b": "b",
    }
    return any(str(item.get(k, "")).strip().lower() == v for k, v in pairs.items())


def explain_noise(item: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if is_synthetic_source(item.get("source", "")):
        reasons.append(f"source={item.get('source')}")
    for k in ("source_a", "source_b", "domain", "tags", "metadata"):
        if is_synthetic_source(item.get(k, "")):
            reasons.append(f"synthetic_{k}")
    for k, v in (("claim", "claim"), ("claim_a", "x"), ("claim_b", "y"), ("missing_evidence", "proof"), ("reason", "reason"), ("source_a", "a"), ("source_b", "b")):
        if str(item.get(k, "")).strip().lower() == v:
            reasons.append(f"{k}={v}")
    text = _flat_text(item)
    if any(tok in text for tok in PLACEHOLDER_TOKENS):
        reasons.append("placeholder_token")
    if text.count("absent") > 2:
        reasons.append("too_many_absent")
    if text.count("inconnu") > 2:
        reasons.append("too_many_inconnu")
    if "client cherche plombier lyon fuite urgente" in text and is_synthetic_source(item):
        reasons.append("demo_lyon_plombier")
    return sorted(set(reasons))


def is_demo_or_test_item(item: dict[str, Any]) -> bool:
    return len(explain_noise(item)) > 0


def classify_noise(item: dict[str, Any]) -> dict[str, Any]:
    reasons = explain_noise(item)
    is_noise = len(reasons) > 0
    noise_type = "REAL_ITEM"
    if is_noise:
        if any(r.startswith("claim") or r.startswith("source_a=") or r.startswith("source_b=") for r in reasons):
            noise_type = "TEST_PLACEHOLDER_CONFLICT"
        elif "missing_evidence=proof" in reasons:
            noise_type = "TEST_PLACEHOLDER_UNCERTAINTY"
        elif any("synthetic" in r or r.startswith("source=") for r in reasons):
            noise_type = "DEMO_OR_TEST_ITEM"
        else:
            noise_type = "PLACEHOLDER_CONTENT"
    return {
        "is_noise": is_noise,
        "noise_type": noise_type,
        "reasons": reasons,
        "safe_to_exclude_from_health": is_noise,
        "safe_to_exclude_from_canon": is_noise,
    }


def should_count_as_real(item: dict[str, Any]) -> bool:
    return not classify_noise(item)["is_noise"]


def filter_real_items(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [i for i in items if should_count_as_real(i)]


def filter_noise_items(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [i for i in items if not should_count_as_real(i)]
