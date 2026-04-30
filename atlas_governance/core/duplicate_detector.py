from collections import defaultdict
from .common import iter_project_files, repo_root, sha256_file, write_json, write_md, runtime_dir

def run_duplicate_detection():
    root=repo_root(); by=defaultdict(list)
    for p in iter_project_files(include_runtime=False):
        by[sha256_file(p)].append(str(p.relative_to(root)))
    groups=[g for g in by.values() if len(g)>1]
    out={"count":len(groups),"duplicate_groups":groups}
    write_json(runtime_dir()/"reports/duplicates.json",out)
    write_md(runtime_dir()/"reports/duplicates.md","# Duplicates\n"+"\n".join([", ".join(g) for g in groups]))
    return out
