import json
from datetime import datetime
from .config import BASE

def log_query_run(run_payload):
    p = BASE / "runtime/query_lab"
    p.mkdir(parents=True, exist_ok=True)
    line = {"timestamp": datetime.utcnow().isoformat(), **run_payload}
    with (p / "query_runs.jsonl").open("a", encoding="utf-8") as f:
        f.write(json.dumps(line, ensure_ascii=False) + "\n")
