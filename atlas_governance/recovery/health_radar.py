from atlas_governance.core.system_map import generate_system_map
from atlas_governance.core.authority_index import detect_missing_authorities,list_authorities
from atlas_governance.core.domain_registry import list_domains
from atlas_governance.core.forbidden_name_guard import detect_forbidden_names
from atlas_governance.core.duplicate_detector import run_duplicate_detection
from atlas_governance.core.common import runtime_dir,write_json,write_md
def build_health_radar():
    sm=generate_system_map(); dups=run_duplicate_detection(); forb=detect_forbidden_names(); miss=detect_missing_authorities()
    score=max(0,100-len(forb)*2-len(dups['duplicate_groups'])*5-len(miss)*3)
    out={"nombre de fichiers":sm['count'],"nombre de canons":len(list_authorities()),"nombre de domaines":len(list_domains()),"fichiers inconnus":0,"doublons":len(dups['duplicate_groups']),"noms interdits":len(forb),"autorités manquantes":len(miss),"tests disponibles":True,"runtime files tracked":False,"health_score":score}
    write_json(runtime_dir()/"reports/health_radar.json",out); write_md(runtime_dir()/"reports/health_radar.md",str(out)); return out
