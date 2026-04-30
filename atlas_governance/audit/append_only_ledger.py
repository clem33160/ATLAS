from . import *
from atlas_governance.core.common import runtime_dir, now_iso
import json
LEDGER=runtime_dir()/"audit/ledger.jsonl"
def append_event(event_type, actor='agent', command='', files_touched=None, domain='navigation', decision='', status='OK', notes=''):
    LEDGER.parent.mkdir(parents=True, exist_ok=True); rec={"timestamp":now_iso(),"event_type":event_type,"actor":actor,"command":command,"files_touched":files_touched or [],"domain":domain,"decision":decision,"status":status,"notes":notes};
    with LEDGER.open('a',encoding='utf-8') as f:f.write(json.dumps(rec,ensure_ascii=False)+"\n")
    return rec
def read_recent_events(limit=20):
    if not LEDGER.exists(): return []
    return [json.loads(l) for l in LEDGER.read_text(encoding='utf-8').splitlines()[-limit:]]
def summarize_ledger(): return {"events":len(read_recent_events(1000))}
