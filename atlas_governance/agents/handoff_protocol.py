import json
from atlas_governance.core.common import runtime_dir
def append_handoff(record):
    p=runtime_dir()/"audit/agent_handoffs.jsonl"; p.parent.mkdir(parents=True, exist_ok=True)
    with p.open('a',encoding='utf-8') as f:f.write(json.dumps(record,ensure_ascii=False)+"\n")
