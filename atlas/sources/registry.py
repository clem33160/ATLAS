from pathlib import Path


def load_sources_config(path: Path) -> str:
    return path.read_text(encoding='utf-8')
