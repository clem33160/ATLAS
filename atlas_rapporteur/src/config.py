import json, os
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]

def load_json(rel):
    return json.loads((BASE / rel).read_text(encoding='utf-8'))

def env(name, default=None):
    return os.getenv(name, default)
