from __future__ import annotations
from pathlib import Path
from .common import read_json

def run_doctrine_check()->dict:
    doctrine=read_json(Path('atlas_memory/config/memory_doctrine.json'),{})
    layers=doctrine.get('layers',[])
    questions=doctrine.get('seven_questions',[])
    ok=len(layers)==20 and len(questions)==7
    return {'doctrine_ok':ok,'layers_count':len(layers),'questions_count':len(questions)}
