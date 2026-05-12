from __future__ import annotations

from pathlib import Path


class LocalStorage:
    def __init__(self, root: str = "~/atlas_data/storage"):
        self.root = Path(root).expanduser()
        self.root.mkdir(parents=True, exist_ok=True)

    def put(self, key: str, data: bytes) -> Path:
        path = self.root / key
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        return path


class S3CompatibleStorage:
    def __init__(self, endpoint: str, bucket: str):
        self.endpoint = endpoint
        self.bucket = bucket

    def put(self, key: str, data: bytes) -> str:
        return f"s3://{self.bucket}/{key}"
