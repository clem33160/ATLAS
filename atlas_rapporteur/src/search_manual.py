import csv
from pathlib import Path
from .config import BASE

def search_manual():
    p = BASE / 'inbox/manual_urls.csv'
    with p.open(encoding='utf-8') as f:
        return list(csv.DictReader(f))
