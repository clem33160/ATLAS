from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from .common import RUNTIME_PATHS, ensure_runtime_structure, read_json, read_jsonl, write_json
from .noise_guard import classify_noise, filter_noise_items, filter_real_items


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("", encoding="utf-8")
    with path.open("a", encoding="utf-8") as h:
        for row in rows:
            h.write(json.dumps(row, ensure_ascii=False) + "\n")


def quarantine_noise() -> dict[str, Any]:
    ensure_runtime_structure()
    noise_dir = RUNTIME_PATHS["raw"].parents[1] / "noise"
    noise_dir.mkdir(parents=True, exist_ok=True)
    mapping = {
        "raw": "quarantined_raw.jsonl",
        "semantic": "quarantined_semantic.jsonl",
        "conflict": "quarantined_conflicts.jsonl",
        "uncertainty": "quarantined_uncertainties.jsonl",
        "audit": "quarantined_audit.jsonl",
        "objectives": "quarantined_objectives.jsonl",
        "procedures": "quarantined_procedures.jsonl",
    }
    counts: dict[str, Any] = {"quarantined_noise_count": 0, "real_items_kept": 0}
    by_reason: dict[str, int] = {}
    for key, qfile in mapping.items():
        rows = read_jsonl(RUNTIME_PATHS[key])
        real = filter_real_items(rows)
        noise = filter_noise_items(rows)
        _write_jsonl(RUNTIME_PATHS[key], real)
        wrapped = [{"item": n, "classification": classify_noise(n)} for n in noise]
        _write_jsonl(noise_dir / qfile, wrapped)
        counts[f"{key}_before"] = len(rows)
        counts[f"{key}_after"] = len(real)
        counts[f"{key}_quarantined"] = len(noise)
        counts["quarantined_noise_count"] += len(noise)
        counts["real_items_kept"] += len(real)
        for n in wrapped:
            for r in n["classification"]["reasons"]:
                by_reason[r] = by_reason.get(r, 0) + 1

    summary_input = json.dumps(counts, sort_keys=True).encode("utf-8")
    counts["summary_hash"] = hashlib.sha256(summary_input).hexdigest()
    counts["top_noise_reasons"] = sorted(by_reason.items(), key=lambda x: x[1], reverse=True)[:10]
    write_json(noise_dir / "quarantine_report.json", counts)
    (noise_dir / "quarantine_report.md").write_text("\n".join([
        "# Quarantine report",
        *(f"- {k}: {v}" for k, v in counts.items() if k != "top_noise_reasons"),
        "- top_noise_reasons:",
        *(f"  - {k}: {v}" for k, v in counts["top_noise_reasons"]),
        "- user_real_data_deleted: false",
    ]), encoding="utf-8")
    return counts
