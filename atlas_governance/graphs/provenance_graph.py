from atlas_governance.core.common import runtime_dir,write_json
def build_provenance_graph(): out={"records":"not_available"}; write_json(runtime_dir()/"graphs/provenance_graph.json",out); return out
