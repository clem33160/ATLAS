from atlas_governance.core.common import runtime_dir,write_json,write_md
def generate_capsule(objective='navigation hardening',domain='governance'):
    c={"objectif demandé":objective,"domaine concerné":domain,"fichiers autorisés":["atlas_governance"],"fichiers interdits":[".git"],"canon actif":["atlas_governance/config/atlas_manifest_core.json"],"tests obligatoires":["atlas_test.sh"],"risques":["scope drift"],"règles anti-destruction":["no destructive delete"]}
    write_json(runtime_dir()/"capsules/agent_context_capsule.json",c); write_md(runtime_dir()/"capsules/agent_context_capsule.md",str(c)); return c
