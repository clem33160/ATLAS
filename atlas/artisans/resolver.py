import json
from pathlib import Path
from .manual_loader import load_csv, load_json
from .official_sources import load_official_urls

def resolve_artisans(base: Path):
    data=[]; warnings=[]
    for a in load_json(base/'data'/'artisans'/'demo_artisans.json'):
        a['source_kind']='DEMO'; a['phone']='NON_PUBLIC'; a['website']='INCONNU'; a['rating']='INCONNU'; a['reviews_count']='INCONNU'; data.append(a)
    for a in load_csv(base/'inbox'/'artisans_manual.csv')+load_json(base/'inbox'/'artisans_manual.json'):
        a['source_kind']='MANUAL'; a['phone']=a.get('phone',''); a['website']=a.get('website','')
        if not a.get('source_url'): warnings.append({'name':a.get('name',''),'warning':'artisan manuel non vérifié'})
        data.append(a)
    for o in load_official_urls(base/'inbox'/'artisans_real_urls.txt'):
        data.append({'name':'Profil officiel fourni','city':'','trades':[],'phone':'','website':'','source_url':o['source_url'],'source_kind':'OFFICIAL_DIRECTORY'})
    (base/'runtime'/'artisans').mkdir(parents=True,exist_ok=True)
    (base/'runtime'/'artisans'/'artisans_resolved.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    (base/'runtime'/'artisans'/'artisan_warnings.json').write_text(json.dumps(warnings,ensure_ascii=False,indent=2),encoding='utf-8')
    return data,warnings
