from __future__ import annotations
from core.documents.classifier import classify

def extract_metadata(doc_id: str, filename: str, text: str, sha256: str, provenance: dict) -> dict:
    return {"doc_id": doc_id, "type": classify(filename, text), "sector": "artisan_plomberie", "client": "", "company": "", "amount_ht": None, "tva_rate": None, "tva_amount": None, "amount_ttc": None, "location": "", "date_doc": "", "source": provenance.get("source", "unknown"), "sensitivity": "normal", "sha256": sha256, "provenance": provenance, "confidence": 0.7}
