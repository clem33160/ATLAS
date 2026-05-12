from __future__ import annotations

from core.global_scale.estimator import estimate_scale
from core.global_scale.extreme_numbers import scientific_notation


def global_scale_report(target_entities: int = 0, target_persons: int = 0) -> str:
    est = estimate_scale(target_entities=target_entities, target_persons=target_persons, average_identifiers_per_entity=2, average_identifiers_per_person=2, average_documents_per_entity=5, average_documents_per_person=5, average_health_docs_per_person=3, average_knowledge_edges_per_entity=10, average_knowledge_edges_per_person=10, average_audit_events_per_entity=5, average_audit_events_per_person=5, average_entity_record_kb=2, average_person_record_kb=2, average_identifier_record_kb=0.5, average_document_metadata_kb=1, average_document_file_kb=10, average_health_metadata_kb=1, average_edge_record_kb=0.5, replication_factor=3, backup_factor=2, regions=3, read_queries_per_entity_per_month=5, read_queries_per_person_per_month=5, write_events_per_entity_per_month=2, write_events_per_person_per_month=2)
    if target_entities >= 10**12:
        return "\n".join(["ATLAS EXTREME THEORETICAL SCALE MODEL", f"Target entities: {target_entities:,}", f"Scientific notation: {scientific_notation(target_entities)}", "Architecture tier: Tier 6", "Production-ready: NO", "Model type: theoretical stress model only"])
    if target_persons:
        return "\n".join(["ATLAS GLOBAL PERSON/HEALTH SCALE MODEL", f"Target persons: {target_persons:,}", f"Total person identifiers: {est.total_identifiers:,}", f"Total health document metadata records: {est.total_health_documents:,}", f"Consent records required: {target_persons:,}", f"Audit events estimated: {est.total_audit_events:,}", f"Estimated storage: {est.total_primary_storage:.2f} PB", "Suggested architecture tier: Tier 5", "Atlas Health production-ready: NO", "Health architecture model ready: YES"])
    return "\n".join(["ATLAS GLOBAL ENTITY SCALE MODEL", f"Target entities: {target_entities:,}", f"Total identifiers: {est.total_identifiers:,}", f"Total documents: {est.total_documents:,}", f"Total knowledge edges: {est.total_knowledge_edges:,}", f"Total audit events: {est.total_audit_events:,}", f"Estimated primary storage: {est.total_primary_storage:.2f} PB", f"Estimated replicated storage: {est.total_replicated_storage:.2f} PB", f"Estimated backup storage: {est.total_backup_storage:.2f} PB", "Suggested architecture tier: Tier 4", "Production-ready for 2B entities: NO", "Architecture model ready: YES"])
