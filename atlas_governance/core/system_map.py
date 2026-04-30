from .common import iter_project_files, repo_root, runtime_dir, sha256_file, write_json, write_md

def _role(rel: str) -> str:
    if rel.startswith("atlas_governance/runtime/"):
        return "runtime"
    if "/tests/" in rel or rel.startswith("tests/"):
        return "test"
    if "/scripts/" in rel:
        return "script"
    if "/config/" in rel or rel.endswith(".json"):
        return "config"
    if rel.endswith(".py"):
        return "source"
    return "unknown"

def generate_system_map():
    root = repo_root()
    entries=[]
    counts={"unknown":0,"canon":0,"script":0,"config":0,"test":0,"runtime":0}
    for p in iter_project_files(include_runtime=True):
        rel=str(p.relative_to(root))
        role=_role(rel)
        if role in counts: counts[role]+=1
        if role in ("source","config"): counts["canon"]+=1
        entries.append({"path":rel,"role":role,"hash":sha256_file(p)})
    out={"count":len(entries),"counts":counts,"files":entries[:5000]}
    write_json(runtime_dir()/"maps/system_map.json",out)
    write_md(runtime_dir()/"maps/system_map.md","# System map\n"+"\n".join(f"- {k}: {v}" for k,v in counts.items()))
    return out
