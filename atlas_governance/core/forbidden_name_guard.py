from .common import repo_root, FORBIDDEN_TOKENS, read_json

def detect_forbidden_names():
    root = repo_root()
    auth = read_json(root / "atlas_governance/config/atlas_authority_index.json", {}) or {}
    out = []
    for rel in [v for v in auth.values() if isinstance(v, str)]:
        low = rel.lower()
        if any(t in low for t in FORBIDDEN_TOKENS):
            out.append(rel)
    return out

def validate_no_forbidden_canon():
    f = detect_forbidden_names()
    return {"ok": len(f) == 0, "forbidden": f}
