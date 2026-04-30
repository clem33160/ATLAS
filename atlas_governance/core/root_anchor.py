from pathlib import Path
from .common import repo_root

def find_root(start=None):
    return repo_root(Path(start) if start else None)
