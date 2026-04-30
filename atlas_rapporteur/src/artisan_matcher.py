import csv
from .config import BASE


def match_artisans(lead, max_n=5):
    rows = []
    with (BASE / "inbox/manual_artisans.csv").open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r.get("trade") != lead.trade:
                continue
            if lead.city != "INCONNU" and r.get("city") != lead.city:
                continue
            website = r.get("website") or "ABSENT"
            phone = r.get("phone") or "ABSENT"
            if r.get("source_url") in (None, ""):
                continue
            match_score = 80 if r.get("city") == lead.city else 60
            rows.append({
                "name": r.get("name", "ABSENT"), "trade": r.get("trade", "INCONNU"), "city": r.get("city", "INCONNU"),
                "country": r.get("country", "INCONNU"), "phone": phone, "website": website, "source_url": r.get("source_url"),
                "source_type": r.get("source_type", "manual"), "verification_status": r.get("verification_status", "TO_VALIDATE"),
                "confidence": float(r.get("confidence", 0.5)), "match_score": match_score
            })
    lead.matched_artisans = sorted(rows, key=lambda x: x["match_score"], reverse=True)[:max_n]
    return lead
