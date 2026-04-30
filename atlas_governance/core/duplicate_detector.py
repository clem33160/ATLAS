from collections import defaultdict
from pathlib import Path
from .common import project_root, sha256_file, write_json, write_md, runtime_dir

def run_duplicate_detection():
    by=defaultdict(list)
    for p in project_root().rglob('*'):
        if p.is_file() and '.git/' not in str(p): by[sha256_file(p)].append(str(p.relative_to(project_root())))
    d=[v for v in by.values() if len(v)>1]
    out={"duplicate_groups":d,"count":len(d)}
    write_json(runtime_dir()/"reports/duplicates.json",out)
    write_md(runtime_dir()/"reports/duplicates.md","# Duplicates\n"+"\n".join([", ".join(g) for g in d]))
    return out
