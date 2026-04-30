from .duplicate_detector import run_duplicate_detection
from .common import write_json, runtime_dir

def neutralize_variants():
    d=run_duplicate_detection(); marks=[]
    for g in d['duplicate_groups']:
        for p in g[1:]: marks.append({"path":p,"status":"NON_CANONICAL_VARIANT"})
    out={"marked":marks}
    write_json(runtime_dir()/"reports/variant_neutralization.json",out)
    return out
