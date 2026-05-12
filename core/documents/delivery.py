from __future__ import annotations
from pathlib import Path
import hashlib, shutil
from core.access.checks import can_access
from core.proof.receipt import build_receipt

def deliver(doc: dict, role: str, out_dir: Path, category: str) -> dict:
    if not can_access(role, category):
        raise PermissionError("access denied")
    src = Path(doc["path"])
    current = hashlib.sha256(src.read_bytes()).hexdigest()
    if current != doc["sha256"]:
        raise PermissionError("hash changed")
    out_dir.mkdir(parents=True, exist_ok=True)
    dst = out_dir / src.name
    shutil.copy2(src, dst)
    return build_receipt(role, doc["doc_id"], str(src), str(dst), doc["sha256"], "delivered", doc.get("provenance", {}))
