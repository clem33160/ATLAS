from __future__ import annotations

TYPES = ["facture_client","facture_fournisseur","devis","contrat_client","urssaf","impot","tva","dette_relance","recu","rib","bulletin_salaire","assurance","document_personnel","a_verifier"]


def classify(filename: str, text: str) -> str:
    f = filename.lower(); t = text.lower()
    if "devis" in f: return "devis"
    if "facture" in f and "fournisseur" in f: return "facture_fournisseur"
    if "facture" in f: return "facture_client"
    if "rib" in f or "iban" in t: return "rib"
    if "urssaf" in f+t: return "urssaf"
    if "bulletin" in f+t: return "bulletin_salaire"
    if "contrat" in f+t: return "contrat_client"
    if "relance" in f+t or "impay" in t: return "dette_relance"
    if "recu" in f+t: return "recu"
    if "tva" in f and "facture" not in f: return "tva"
    if "impot" in f+t: return "impot"
    if "assurance" in f+t: return "assurance"
    return "a_verifier"
