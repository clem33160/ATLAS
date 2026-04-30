from .common import project_root, FORBIDDEN_TOKENS

def detect_forbidden_names():
    out=[]
    for p in project_root().rglob('*'):
        if p.is_file() and '.git/' not in str(p):
            low=p.name.lower()
            if any(t in low for t in FORBIDDEN_TOKENS): out.append(str(p.relative_to(project_root())))
    return out
def validate_no_forbidden_canon(): return {"ok":len(detect_forbidden_names())==0,"forbidden":detect_forbidden_names()}
def explain_forbidden_name(path):
    s=str(path).lower(); return [t for t in FORBIDDEN_TOKENS if t in s]
