#!/usr/bin/env python3
import csv,json,sys
from pathlib import Path

inp,md,csvp,jsp,real_count,stub_count,stub_names=sys.argv[1:8]
rows=[json.loads(l) for l in open(inp,encoding='utf-8') if l.strip()]
Path(md).parent.mkdir(parents=True,exist_ok=True)
kept=[r for r in rows if r['verdict']!='A_REJETER']
counts={k:sum(1 for r in kept if r['size']==k) for k in ['PETIT','MOYEN','GROS','TITAN']}
comm=sum(r.get('commission_eur') or 0 for r in kept)
with open(jsp,'w',encoding='utf-8') as o:
  for r in rows:o.write(json.dumps(r,ensure_ascii=False)+"\n")
fields=['lead_id','source_name','title','url','published_date','age_days','domain','amount_eur','commission_eur','size','score','verdict']
with open(csvp,'w',newline='',encoding='utf-8') as c:
  w=csv.DictWriter(c,fieldnames=fields);w.writeheader();[w.writerow({k:r.get(k) for k in fields}) for r in rows]
missing=max(0,50-len(kept))
with open(md,'w',encoding='utf-8') as m:
  m.write('# Atlas Rapporteur V1 - Leads du jour\n\nRésumé :\n')
  m.write(f"- leads trouvés : {len(rows)}\n- leads retenus : {len(kept)}\n- commission théorique totale : {comm:.2f} €\n")
  m.write(f"- petits : {counts['PETIT']}\n- moyens : {counts['MOYEN']}\n- gros : {counts['GROS']}\n- titans : {counts['TITAN']}\n")
  m.write(f"- leads manquants pour 50/jour : {missing}\n")
  m.write(f"- connecteurs réels : {real_count}\n- connecteurs stubs : {stub_count}\n")
  if missing>0:
    m.write(f"- Objectif 50/jour non atteint car seuls {real_count} connecteurs réels sont implémentés.\n")
    m.write(f"- Sources à implémenter ensuite : {stub_names}.\n")
    m.write('- Prochaine action : implémenter un connecteur public robuste supplémentaire puis recalibrer scoring.\n')
  m.write('\n## Top leads\n\n')
  for i,r in enumerate(sorted(kept,key=lambda x:x['score'], reverse=True)[:10],1):
    m.write(f"### Lead {i}\n- Titre : {r['title']}\n- Source : {r['source_name']}\n- URL : {r['url']}\n- Domaine : {r['domain']}\n- Montant : {r.get('amount_eur','A_VERIFIER')}\n- Commission 5 % : {r.get('commission_eur','A_VERIFIER')}\n- Taille : {r['size']}\n- Score : {r['score']}\n- Pourquoi c’est intéressant : {', '.join(r['score_reasons']) or 'A_VERIFIER'}\n- Ce qu’il faut vérifier : montant exact, éligibilité, périmètre technique\n- Action humaine : qualification commerciale manuelle\n- Verdict : {r['verdict']}\n\n")
print(f"report_markdown={md}")
