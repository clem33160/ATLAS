from __future__ import annotations
from pathlib import Path

from .raw_store import append_event
from .common import new_id, now_iso
from .common import read_json, read_jsonl
from . import semantic_store, uncertainty_store, conflict_store, simulation_store, social_store, causal_store


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


def _ingest_lead_payload(leads_payload: list[dict]) -> int:
    accepted = 0
    for lead in leads_payload:
        status = lead.get("qualification_status") or lead.get("tier")
        if status != "TO_VALIDATE":
            continue
        ev = create_system_event("lead_accepted", "rapporteur_affaires", lead.get("title", "lead accepted"), 0.76, {"url": lead.get("url", "")})
        facts = semantic_store.extract_semantic_facts({"event_id": ev["event_id"], "domain": "rapporteur_affaires", "content": lead.get("snippet", ""), "source": "system"})
        semantic_store.append_concepts(ev["event_id"], facts)
        accepted += 1
    return accepted


def ingest_rapporteur_run(summary_path=None, rejected_path=None, leads_path=None):
    res = {}
    summary_p = Path(summary_path or 'atlas_rapporteur/runtime/reports/daily_report.json')
    rejected_p = Path(rejected_path or 'atlas_rapporteur/runtime/audit/rejected_results.json')
    leads_p = Path(leads_path or 'atlas_rapporteur/runtime/exports/leads_ranked.json')

    if summary_p.exists():
        payload = read_json(summary_p, {})
        create_system_event('rapporteur_ingest', 'rapporteur_affaires', 'summary ingested', 0.9, payload)
        res['summary'] = 'ingested'
    else:
        res['summary'] = 'missing'

    if leads_p.exists():
        leads = read_json(leads_p, [])
        accepted = _ingest_lead_payload(leads if isinstance(leads, list) else [])
        res['leads'] = f'ingested:{accepted}'
    else:
        res['leads'] = 'missing'

    if rejected_p.exists():
        rejected = read_json(rejected_p, [])
        for item in rejected[:20]:
            reason = str(item.get("reason", ""))
            if "CONFLICT" in reason:
                conflict_store.open_conflict("provider", "quality_gate", item.get("title", "?"), reason, "rapporteur_affaires")
            else:
                uncertainty_store.add_uncertainty("rapporteur_affaires", item.get("title", "unknown"), reason or "needs review", 0.4)
        res['rejected'] = f'ingested:{len(rejected)}'
    else:
        res['rejected'] = 'missing'

    raw_events = read_jsonl(Path('atlas_memory/runtime/raw/events.jsonl'))
    causal_store.persist_causal_links(causal_store.infer_causal_links(raw_events[-30:]))
    return res


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
