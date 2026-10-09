from __future__ import annotations

from .raw_store import append_event
from .common import new_id, now_iso
from . import simulation_store, social_store


def create_system_event(kind, domain, content, confidence, metadata=None):
    return append_event({
        'event_id': new_id('evt'),
        'timestamp': now_iso(),
        'kind': kind,
        'domain': domain,
        'content': content,
        'source': 'system',
        'confidence': confidence,
        'metadata': metadata or {},
    })


def ingest_governance_health():
    from atlas_governance.core.invariant_engine import run_invariants
    invariants = run_invariants()
    ev = create_system_event('governance_decision', 'governance', 'governance health ingested', 0.8, invariants)
    simulation_store.add_scenario(
        title='governance hardening',
        assumptions=['invariants maintained'],
        expected_outcomes=['lower confusion'],
        risks=['false positives in guards'],
        cost=1.0,
        benefit=2.5,
        confidence=0.7,
        domain='governance',
    )
    social_store.record_social_signal('governance_update', 'atlas_ops', 'governance health recorded', consent_explicit=True)
    return ev


def ingest_test_result(module, passed, warnings=0):
    return create_system_event('test_result', module, f'passed={passed} warnings={warnings}', 0.8 if passed else 0.4)
