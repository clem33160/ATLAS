from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from core.global_scale.estimator import estimate_scale
from core.global_scale.identifier_model import build_identifier, global_atlas_entity_id, global_atlas_person_id, has_duplicate_identifiers


@dataclass
class ProofGlobalScale:
    CRITICAL_FAIL: int


def shard_for(value: str, shards: int = 64) -> int:
    return sum(value.encode("utf-8")) % shards


def run_proof_global_scale(base: Path) -> ProofGlobalScale:
    base.mkdir(parents=True, exist_ok=True)
    ids = [build_identifier(identifier_type="SIRET", identifier_value=f"A-{i}", country="FR", jurisdiction="FR-75", source_id="synthetic", provenance="proof", confidence=0.9, last_seen_at="2026-01-01T00:00:00Z") for i in range(100)]
    if has_duplicate_identifiers(ids):
        return ProofGlobalScale(CRITICAL_FAIL=1)
    est = estimate_scale(target_entities=2_000_000_000, target_persons=15_000_000_000, average_identifiers_per_entity=2, average_identifiers_per_person=2, average_documents_per_entity=5, average_documents_per_person=5, average_health_docs_per_person=3, average_knowledge_edges_per_entity=10, average_knowledge_edges_per_person=10, average_audit_events_per_entity=5, average_audit_events_per_person=5, average_entity_record_kb=2, average_person_record_kb=2, average_identifier_record_kb=0.5, average_document_metadata_kb=1, average_document_file_kb=10, average_health_metadata_kb=1, average_edge_record_kb=0.5, replication_factor=3, backup_factor=2, regions=3, read_queries_per_entity_per_month=5, read_queries_per_person_per_month=5, write_events_per_entity_per_month=2, write_events_per_person_per_month=2)
    if est.production_ready_claim != "NO":
        return ProofGlobalScale(CRITICAL_FAIL=1)
    _ = global_atlas_entity_id("entity-1"), global_atlas_person_id("person-1"), shard_for("FR:75")
    return ProofGlobalScale(CRITICAL_FAIL=0)
