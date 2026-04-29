#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
import json
from pathlib import Path
p=Path('atlas/config/real_sources.yaml')
lines=p.read_text(encoding='utf-8').splitlines()
sources=[]; cur={}
for line in lines:
    s=line.strip()
    if s.startswith('- source_id:'):
        if cur: sources.append(cur)
        cur={'source_id':s.split(':',1)[1].strip()}
    elif cur and ':' in s and not s.startswith('#'):
        k,v=s.split(':',1); cur[k.strip()]=v.strip().strip('"')
if cur: sources.append(cur)
enabled=[x for x in sources if x.get('enabled_default')=='true']
disabled=[x for x in sources if x.get('enabled_default')!='true']
off=[x for x in sources if x.get('reliability_level')=='official']
tos=[x for x in sources if x.get('requires_human_tos_validation')=='true']
viol=[x['source_id'] for x in sources if x.get('reliability_level')=='private_candidate' and x.get('enabled_default')=='true' and x.get('human_validated_tos')!='true']
print(f"Sources total: {len(sources)}")
print(f"Activées: {len(enabled)}")
print(f"Désactivées: {len(disabled)}")
print('Officielles:', ', '.join(x['source_id'] for x in off))
print('Validation CGU requise:', ', '.join(x['source_id'] for x in tos))
if viol:
    print('ERREUR:', ', '.join(viol)); raise SystemExit(2)
Path('atlas/runtime/export').mkdir(parents=True,exist_ok=True)
Path('atlas/runtime/export/sources_audit.json').write_text(json.dumps({'total':len(sources),'violations':viol},indent=2),encoding='utf-8')
PY
