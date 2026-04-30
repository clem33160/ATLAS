from .common import suspicious_name

def classify(path):
    p=str(path).lower()
    if "/runtime/" in p: return "RUNTIME"
    if "/tests/" in p or p.endswith("_test.py"): return "TEST"
    if p.endswith(".sh"): return "SCRIPT"
    if p.endswith(".json") or "/config/" in p: return "CONFIG"
    if suspicious_name(p): return "ARCHIVE"
    if p.endswith('.log'): return 'LOG'
    return "UNKNOWN"
