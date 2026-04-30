from pathlib import Path
from .common import project_root, write_json, write_md, sha256_file, runtime_dir
from .file_role_classifier import classify
from .domain_registry import assign_path_to_domain
from .path_resolver import is_canonical_path

def generate_system_map():
    entries=[]
    for p in project_root().rglob('*'):
        if not p.is_file() or '.git/' in str(p): continue
        rel=str(p.relative_to(project_root()))
        entries.append({"path":rel,"role":classify(rel),"domain":assign_path_to_domain(rel),"size":p.stat().st_size,"modified_time":p.stat().st_mtime,"hash_sha256":sha256_file(p),"canonical_status":"CANON" if is_canonical_path(rel) else "NON_CANON","suspicious_name":not is_canonical_path(rel),"authority_match":rel.endswith('atlas_manifest_core.json'),"generated_or_source":"generated" if '/runtime/' in rel else 'source','notes':''})
    j=runtime_dir()/"maps/system_map.json"; m=runtime_dir()/"maps/system_map.md"
    write_json(j,{"files":entries,"count":len(entries)})
    write_md(m,"# System Map\n\n"+"\n".join(f"- {e['path']} [{e['role']}]" for e in entries[:200]))
    return {"json":str(j),"md":str(m),"count":len(entries)}
