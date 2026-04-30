from atlas_governance.core.common import project_root,runtime_dir,write_json,write_md
def build_dependency_graph():
    nodes=[]
    for p in project_root().rglob('*.py'):
        if '.git/' in str(p): continue
        nodes.append(str(p.relative_to(project_root())))
    out={"nodes":nodes,"edges":[]}
    write_json(runtime_dir()/"graphs/dependency_graph.json",out); write_md(runtime_dir()/"graphs/dependency_graph.md","\n".join(nodes)); return out
