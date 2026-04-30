import json
from atlas_governance.core.common import runtime_dir, now_iso
LOG=runtime_dir()/"recovery/blackbox.jsonl"
def write_blackbox(status):
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open('a',encoding='utf-8') as f: f.write(json.dumps({"timestamp":now_iso(),**status})+"\n")
