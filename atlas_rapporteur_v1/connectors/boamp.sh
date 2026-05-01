#!/usr/bin/env bash
set -euo pipefail
OUT=${1:-atlas_rapporteur_v1/runtime/raw/boamp_raw.jsonl}
mkdir -p "$(dirname "$OUT")"
TMP=$(mktemp)
URLS=(
  "https://www.data.gouv.fr/fr/datasets/r/6a77f8d3-0f40-4d75-a4a0-5cbf9f0cc09f"
  "https://www.boamp.fr/api/explore/v2.1/catalog/datasets/avis-de-marche/records?limit=200"
)
ok=0
for u in "${URLS[@]}"; do
  if curl -A "AtlasRapporteurV1/1.0 (+public data use)" -fsSL "$u" -o "$TMP"; then
    echo "{\"event\":\"boamp_fetch_ok\",\"url\":\"$u\"}" >&2
    ok=1
    break
  fi
done
if [ "$ok" -ne 1 ]; then
  echo "{\"event\":\"boamp_fetch_failed\",\"urls\":$(printf '%s\n' "${URLS[@]}" | python3 -c 'import json,sys; print(json.dumps([x.strip() for x in sys.stdin if x.strip()]))')}" >&2
  : > "$OUT"
  rm -f "$TMP"
  exit 0
fi
python3 - "$TMP" "$OUT" <<'PY'
import csv, json, sys
src, out = sys.argv[1], sys.argv[2]
count=0
text=open(src,'r',encoding='utf-8',errors='ignore').read()
with open(out,'w',encoding='utf-8') as o:
    parsed=False
    try:
        obj=json.loads(text)
        records=obj.get('results') or obj.get('records') or []
        for row in records:
            title=(row.get('title') or row.get('objet') or row.get('libelle') or '').strip()
            url=(row.get('url') or row.get('source') or row.get('permalink') or '').strip()
            if not title or not url: continue
            rec={"source_id":"boamp","source_name":"BOAMP Open Data","title":title,"url":url,
                 "published_date":(row.get('published_date') or row.get('dateparution') or '')[:10],
                 "amount_text": row.get('amount') or row.get('valeur') or '',
                 "buyer": row.get('buyer') or row.get('nomacheteur') or '',
                 "location": row.get('location') or row.get('lieuExecution') or ''}
            o.write(json.dumps(rec,ensure_ascii=False)+"\n"); count+=1
        parsed=True
    except Exception:
        pass
    if not parsed:
        for row in csv.DictReader(text.splitlines()):
            url = row.get('url') or row.get('source_url') or ''
            title = row.get('objet') or row.get('title') or ''
            if not url or not title: continue
            rec = {'source_id':'boamp','source_name':'BOAMP Open Data','title':title.strip(),'url':url.strip(),
                   'published_date':(row.get('dateparution') or row.get('publication_date') or '')[:10],
                   'amount_text': row.get('valeur') or row.get('montant') or '','buyer': row.get('nomacheteur') or row.get('acheteur') or '',
                   'location': row.get('lieuExecution') or row.get('codepostal') or ''}
            o.write(json.dumps(rec, ensure_ascii=False)+"\n"); count+=1
print(f"boamp_raw_records={count}")
PY
rm -f "$TMP"
