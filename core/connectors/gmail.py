from __future__ import annotations
import hashlib
from pathlib import Path


def list_messages(api_list_fn, query: str) -> list[dict]:
    return api_list_fn(query)


def search_attachments(messages: list[dict], filename_suffix: str = ".pdf") -> list[dict]:
    out = []
    for m in messages:
        for a in m.get("attachments", []):
            if a.get("filename", "").lower().endswith(filename_suffix):
                out.append({"message": m, "attachment": a})
    return out


def import_pdf_attachments(matches: list[dict], import_dir: Path, fetch_attachment_fn) -> list[dict]:
    import_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    for item in matches:
        msg = item["message"]
        att = item["attachment"]
        content = fetch_attachment_fn(msg["id"], att["id"])
        target = import_dir / att["filename"]
        target.write_bytes(content)
        sha = hashlib.sha256(content).hexdigest()
        rows.append({"message_id": msg["id"], "sender": msg.get("from", ""), "subject": msg.get("subject", ""), "date": msg.get("date", ""), "attachment_id": att["id"], "filename": att["filename"], "sha256": sha, "path": str(target)})
    return rows
