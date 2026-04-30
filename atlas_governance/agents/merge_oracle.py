import subprocess
from atlas_governance.core.common import runtime_dir,write_json,write_md
from atlas_governance.core.duplicate_detector import run_duplicate_detection
def run_merge_oracle():
    try: diff=subprocess.check_output(['git','diff','--name-status'],text=True).splitlines()
    except Exception: diff=[]
    out={"diff":diff,"duplicates":run_duplicate_detection()}
    write_json(runtime_dir()/"reports/merge_oracle.json",out); write_md(runtime_dir()/"reports/merge_oracle.md",str(out)); return out
