from atlas_governance.audit.preflight_navigator import run_preflight
from atlas_governance.core.common import runtime_dir, write_json, write_md
def run_postflight():
    r=run_preflight(); out={"postflight":"ok" if r['manifest']['ok'] else 'fail',"checks":r}
    write_json(runtime_dir()/"reports/postflight_report.json",out); write_md(runtime_dir()/"reports/postflight_report.md",str(out)); return out
