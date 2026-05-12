from __future__ import annotations
import shutil

def ocr_status() -> str:
    return "available" if shutil.which("tesseract") else "unavailable"
