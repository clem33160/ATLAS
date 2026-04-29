from __future__ import annotations

from html.parser import HTMLParser
from urllib.parse import urlparse
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import re

USER_AGENT = "AtlasRapporteurAffaires/0.7 human-supervised"


class _TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        if data and data.strip():
            self.parts.append(data.strip())


def safe_excerpt(text: str, max_chars: int = 1200) -> str:
    return (text or "")[:max_chars]


def normalize_web_text(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").strip())


def extract_text_from_html(html: str) -> str:
    parser = _TextExtractor()
    parser.feed(html or "")
    return normalize_web_text(" ".join(parser.parts))


def fetch_public_url(url: str) -> dict:
    parsed = urlparse((url or "").strip())
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return {"ok": False, "error": "URL invalide", "http_status": None, "raw_html": ""}
    req = Request(url, method="GET", headers={"User-Agent": USER_AGENT})
    try:
        with urlopen(req, timeout=10) as res:
            body = res.read(120000).decode("utf-8", errors="replace")
            return {"ok": True, "http_status": getattr(res, "status", 200), "raw_html": body, "error": ""}
    except HTTPError as exc:
        return {"ok": False, "error": f"HTTPError: {exc}", "http_status": getattr(exc, 'code', None), "raw_html": ""}
    except URLError as exc:
        return {"ok": False, "error": f"URLError: {exc}", "http_status": None, "raw_html": ""}
    except Exception as exc:
        return {"ok": False, "error": f"Fetch error: {exc}", "http_status": None, "raw_html": ""}
