import csv
from datetime import datetime
from .config import BASE

VALID_STATUSES={"À_APPELER","APPELÉ","INTÉRESSÉ","PAS_INTÉRESSÉ","À_RELANCER","DEAL_POTENTIEL","SIGNÉ","PERDU"}

def append_call_update(lead_id,status,comment=''):
    if status not in VALID_STATUSES:
        raise ValueError('invalid status')
    p=BASE/'inbox/call_updates.csv'
    with p.open('a',encoding='utf-8',newline='') as f:
        csv.writer(f).writerow([lead_id,status,datetime.utcnow().isoformat(),comment])
