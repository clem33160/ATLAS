from pathlib import Path
import json

def load_demo_signals(path: Path) -> list[dict]:
    return json.loads(path.read_text(encoding='utf-8'))
