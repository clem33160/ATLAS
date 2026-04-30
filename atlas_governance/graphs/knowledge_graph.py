from atlas_governance.core.common import project_root,runtime_dir,write_json
def build_knowledge_graph():
    rap=project_root()/"atlas_rapporteur"
    out={"status":"not_available" if not rap.exists() else "available"}
    write_json(runtime_dir()/"graphs/knowledge_graph.json",out); return out
