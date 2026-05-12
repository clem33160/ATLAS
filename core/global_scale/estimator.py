from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ScaleEstimate:
    total_entities: int
    total_persons: int
    total_identifiers: int
    total_documents: int
    total_health_documents: int
    total_knowledge_edges: int
    total_audit_events: int
    total_primary_storage: float
    total_replicated_storage: float
    total_backup_storage: float
    estimated_monthly_reads: int
    estimated_monthly_writes: int
    estimated_indexing_workload: int
    estimated_shards: int
    estimated_partitions: int
    suggested_database_strategy: str
    suggested_object_storage_strategy: str
    suggested_search_strategy: str
    suggested_graph_strategy: str
    suggested_queue_strategy: str
    suggested_region_strategy: str
    suggested_compliance_strategy: str
    suggested_security_strategy: str
    warning_level: str
    production_ready_claim: str = "NO"


def estimate_scale(**p: float | int) -> ScaleEstimate:
    entities = int(p.get("target_entities", 0))
    persons = int(p.get("target_persons", 0))
    id_count = entities * int(p.get("average_identifiers_per_entity", 0)) + persons * int(p.get("average_identifiers_per_person", 0))
    docs = entities * int(p.get("average_documents_per_entity", 0)) + persons * int(p.get("average_documents_per_person", 0))
    health_docs = persons * int(p.get("average_health_docs_per_person", 0))
    edges = entities * int(p.get("average_knowledge_edges_per_entity", 0)) + persons * int(p.get("average_knowledge_edges_per_person", 0))
    audit = entities * int(p.get("average_audit_events_per_entity", 0)) + persons * int(p.get("average_audit_events_per_person", 0))
    kb = (
        entities * float(p.get("average_entity_record_kb", 0))
        + persons * float(p.get("average_person_record_kb", 0))
        + id_count * float(p.get("average_identifier_record_kb", 0))
        + docs * float(p.get("average_document_metadata_kb", 0))
        + health_docs * float(p.get("average_health_metadata_kb", 0))
        + edges * float(p.get("average_edge_record_kb", 0))
    )
    primary = kb / (1024 * 1024)
    repl = primary * float(p.get("replication_factor", 1))
    backup = primary * float(p.get("backup_factor", 1))
    reads = int(entities * p.get("read_queries_per_entity_per_month", 0) + persons * p.get("read_queries_per_person_per_month", 0))
    writes = int(entities * p.get("write_events_per_entity_per_month", 0) + persons * p.get("write_events_per_person_per_month", 0))
    scale = max(entities, persons)
    tier = "Tier 6" if scale >= 10**12 else "Tier 5" if persons >= 15_000_000_000 else "Tier 4" if entities >= 2_000_000_000 else "Tier 3"
    return ScaleEstimate(
        entities, persons, id_count, docs, health_docs, edges, audit, primary, repl, backup, reads, writes, edges + docs,
        max(1, scale // 10_000_000), max(1, scale // 5_000_000),
        f"{tier} distributed DB", "Object storage with lifecycle", "Distributed search", "Graph partitioning", "Regional queues",
        "Multi-region residency" if tier in {"Tier 4", "Tier 5", "Tier 6"} else "Single-region",
        "Consent/privacy/legal separation", "Encryption + strict audit", "HIGH" if tier in {"Tier 4", "Tier 5", "Tier 6"} else "MEDIUM"
    )
