from .common import governance_root, read_json

REQUIRED_ABSOLUTE_LAWS = [
    "Atlas ne fait jamais confiance à une seule carte.",
    "Aucun fichier n’est canonique par son nom seul.",
    "Aucun agent ne modifie sans mission contractuelle.",
    "Toute modification doit être réversible ou reconstructible.",
    "Tout chemin important doit passer par le resolver.",
    "Toute autorité doit avoir une preuve.",
    "La carte doit être reconstruisible depuis zéro.",
    "Toute contradiction devient un objet officiel.",
    "Tout fichier inconnu est suspect jusqu’à classification.",
    "Les agents parallèles doivent être verrouillés.",
    "Les tests doivent attaquer la navigation.",
    "Le système doit pouvoir dire “je suis perdu”.",
]

def load_constitution(root=None):
    return read_json(governance_root() / "config/atlas_constitution_core.json", {})

def validate_constitution() -> dict:
    c = load_constitution()
    laws = c.get("absolute_laws", [])
    missing = [l for l in REQUIRED_ABSOLUTE_LAWS if l not in laws]
    return {"ok": len(missing) == 0, "missing_laws": missing, "count": len(laws)}
