import csv, json
from pathlib import Path

def load_csv(path: Path):
    if not path.exists(): return []
    with path.open('r',encoding='utf-8',newline='') as f: return list(csv.DictReader(f))

def load_json(path: Path):
    return json.loads(path.read_text(encoding='utf-8')) if path.exists() else []
