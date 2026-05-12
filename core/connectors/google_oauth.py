from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, UTC
from pathlib import Path
import json


@dataclass
class OAuthToken:
    access_token: str
    refresh_token: str
    expires_at: str


def token_path_from_config(config: dict) -> Path:
    raw = config["paths"]["google_token_path"]
    return Path(raw).expanduser()


def load_token(path: Path) -> OAuthToken:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return OAuthToken(**payload)


def save_token(path: Path, token: OAuthToken) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(token.__dict__, indent=2), encoding="utf-8")


def refresh_access_token(token: OAuthToken, refresh_fn) -> OAuthToken:
    data = refresh_fn(token.refresh_token)
    exp = datetime.now(UTC) + timedelta(seconds=int(data.get("expires_in", 3600)))
    return OAuthToken(access_token=data["access_token"], refresh_token=token.refresh_token, expires_at=exp.isoformat())
