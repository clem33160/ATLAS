from core.global_scale.estimator import estimate_scale


def _base(**overrides):
    params = dict(target_entities=100, target_persons=0, average_identifiers_per_entity=2, average_identifiers_per_person=2, average_documents_per_entity=5, average_documents_per_person=5, average_health_docs_per_person=3, average_knowledge_edges_per_entity=10, average_knowledge_edges_per_person=10, average_audit_events_per_entity=5, average_audit_events_per_person=5, average_entity_record_kb=2, average_person_record_kb=2, average_identifier_record_kb=0.5, average_document_metadata_kb=1, average_document_file_kb=10, average_health_metadata_kb=1, average_edge_record_kb=0.5, replication_factor=3, backup_factor=2, regions=3, read_queries_per_entity_per_month=5, read_queries_per_person_per_month=5, write_events_per_entity_per_month=2, write_events_per_person_per_month=2)
    params.update(overrides)
    return estimate_scale(**params)


def test_2b_entity_model_outputs_expected_counts():
    r = _base(target_entities=2_000_000_000)
    assert r.total_entities == 2_000_000_000


def test_15b_person_model_outputs_expected_counts():
    r = _base(target_entities=0, target_persons=15_000_000_000)
    assert r.total_persons == 15_000_000_000


def test_extreme_bigint_model_does_not_overflow():
    r = _base(target_entities=10**30)
    assert r.total_entities == 10**30


def test_storage_estimates_are_positive():
    r = _base(target_entities=10_000, target_persons=10_000)
    assert r.total_primary_storage > 0 and r.total_replicated_storage > 0 and r.total_backup_storage > 0
