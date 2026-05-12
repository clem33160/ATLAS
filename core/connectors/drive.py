from __future__ import annotations
from pathlib import Path
import hashlib


def list_files(api_list_fn, folder_ids: list[str]) -> list[dict]:
    return api_list_fn(folder_ids)


def import_supported(files: list[dict], inbox: Path, fetch_fn) -> list[dict]:
    inbox.mkdir(parents=True, exist_ok=True)
    out = []
    for f in files:
        name = f["name"].lower()
        if not (name.endswith(".pdf") or name.endswith(".png") or name.endswith(".jpg")):
            continue
        data = fetch_fn(f["id"])
        path = inbox / f["name"]
        path.write_bytes(data)
        out.append({"file_id": f["id"], "filename": f["name"], "sha256": hashlib.sha256(data).hexdigest(), "path": str(path), "provenance": "google_drive"})
    return out
