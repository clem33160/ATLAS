from atlas_governance.recovery.health_radar import build_health_radar
from atlas_governance.core.common import runtime_dir,write_json,write_md
def build_repair_plan():
    h=build_health_radar(); out={"incohérences détectées":h,"gravité":"MEDIUM" if h['health_score']<80 else 'LOW',"ordre sûr de correction":["fix forbidden names","resolve authorities"],"fichiers à neutraliser":[],"tests à lancer":["atlas_test.sh"],"commande suggérée":"bash atlas_governance/scripts/atlas_preflight.sh"}
    write_json(runtime_dir()/"reports/repair_plan.json",out); write_md(runtime_dir()/"reports/repair_plan.md",str(out)); return out
