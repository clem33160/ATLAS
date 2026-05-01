#!/usr/bin/env bash
set -u

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCRIPTS_DIR="$ROOT_DIR/scripts"
RUNTIME_DIR="$ROOT_DIR/runtime"
REPORTS_DIR="$RUNTIME_DIR/reports"
ACTIONS_DIR="$RUNTIME_DIR/actions"
mkdir -p "$REPORTS_DIR" "$ACTIONS_DIR"

TOP_N="${1:-3}"
MIN_AMOUNT="${2:-400}"
COMMISSION_PCT="${3:-5}"
MAX_AGE="${4:-8}"
MIN_SCORE="${5:-2000}"

TS="$(date +%Y%m%d_%H%M%S)"
REPORT="$REPORTS_DIR/atlas_daily_leads_${TS}.md"
CSV="$ACTIONS_DIR/atlas_daily_leads_${TS}.csv"
TMP_LOG="$(mktemp)"

BEST_SCRIPT="$SCRIPTS_DIR/atlas_best_leads.sh"
OUT_JSONL=""
if [[ -x "$BEST_SCRIPT" ]]; then
  "$BEST_SCRIPT" "$TOP_N" "$MIN_AMOUNT" "$COMMISSION_PCT" "$MAX_AGE" "$MIN_SCORE" >"$TMP_LOG" 2>&1 || true
  OUT_JSONL="$(awk -F= '/OUT_JSONL=/{print $2}' "$TMP_LOG" | tail -n1 | tr -d '[:space:]')"
fi

SAFE_JSONL=""
if [[ -n "$OUT_JSONL" ]]; then
  case "$OUT_JSONL" in
    *rejected*|*deep_harvest*) OUT_JSONL="" ;;
  esac
  if [[ -n "$OUT_JSONL" && -f "$OUT_JSONL" ]]; then
    SAFE_JSONL="$OUT_JSONL"
  fi
fi

python3 - "$SAFE_JSONL" "$REPORT" "$CSV" "$COMMISSION_PCT" "$TOP_N" <<'PY'
import csv, json, os, sys
from datetime import datetime, timezone

src, report, csv_path, pct, top_n = sys.argv[1:6]
pct = float(pct)
top_n = int(top_n)

leads = []
if src and os.path.isfile(src):
    with open(src, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except Exception:
                continue
            blob = json.dumps(obj, ensure_ascii=False).lower()
            if "rejected" in blob or "deep_harvest" in blob:
                continue
            status = str(obj.get("status") or obj.get("lead_status") or "").lower()
            if status and "accept" not in status:
                continue
            leads.append(obj)

leads = leads[:top_n]

def getv(o,*keys,default=""):
    for k in keys:
        if k in o and o[k] not in (None,""):
            return o[k]
    return default

def short_title(t):
    t = str(t or "Sans titre").strip()
    return (t[:117] + "...") if len(t) > 120 else t

rows=[]
total=0.0
for o in leads:
    title = short_title(getv(o,"short_title","title"))
    url = str(getv(o,"boamp_url","url","source_url",default=""))
    domain = str(getv(o,"domain","category",default="Inconnu"))
    age = str(getv(o,"age_days","age",default="?"))
    amount = getv(o,"amount_eur","amount","montant",default=0)
    try:
        amount_f = float(str(amount).replace(" ", "").replace(",", "."))
    except Exception:
        amount_f = 0.0
    commission = amount_f * (pct/100.0)
    total += commission
    proof = str(getv(o,"proof","evidence",default="BOAMP à confirmer"))
    value_status = "VERIF_INCOMPLETE"
    if url and amount_f > 0 and domain != "Inconnu" and age != "?":
        value_status = "PARTIAL_OK"
    checks = "Vérifier montant, deadline, URL, métier, localisation, donneur d’ordre"
    verdict = "A_APPELER_APRES_VERIFICATION" if (url and amount_f>0) else "A_REJETER"
    rows.append({
        "titre_court": title,
        "url_boamp": url,
        "domaine": domain,
        "age": age,
        "montant_detecte": f"{amount_f:.2f}",
        "commission_5pct": f"{commission:.2f}",
        "statut_valeur": value_status,
        "preuve": proof,
        "a_verifier": checks,
        "verdict": verdict,
    })

with open(csv_path,"w",newline="",encoding="utf-8") as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0].keys()) if rows else ["titre_court","url_boamp","domaine","age","montant_detecte","commission_5pct","statut_valeur","preuve","a_verifier","verdict"])
    w.writeheader()
    for r in rows:
        w.writerow(r)

with open(report,"w",encoding="utf-8") as f:
    f.write("# Atlas Daily Leads\n\n")
    f.write(f"- Généré le: {datetime.now(timezone.utc).isoformat()}\n")
    f.write(f"- Nombre de leads: {len(rows)}\n")
    f.write(f"- Commission théorique totale: {total:.2f} EUR\n\n")
    for i,r in enumerate(rows,1):
        f.write(f"## Lead {i} — {r['titre_court']}\n")
        f.write(f"- URL BOAMP: {r['url_boamp']}\n")
        f.write(f"- Domaine: {r['domaine']}\n")
        f.write(f"- Âge: {r['age']}\n")
        f.write(f"- Montant détecté: {r['montant_detecte']} EUR\n")
        f.write(f"- Commission à 5 %: {r['commission_5pct']} EUR\n")
        f.write(f"- Statut valeur: {r['statut_valeur']}\n")
        f.write(f"- Preuve: {r['preuve']}\n")
        f.write(f"- Vérifications humaines: {r['a_verifier']}\n")
        f.write(f"- Verdict: {r['verdict']}\n\n")
    if len(rows) < top_n:
        f.write(f"\n> Moins de {top_n} leads valides trouvés. Sortie conservée avec verdict honnête.\n")

print(f"OUT_REPORT={report}")
print(f"OUT_CSV={csv_path}")
PY

rm -f "$TMP_LOG"
exit 0
