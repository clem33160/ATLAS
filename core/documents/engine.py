from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DocumentProof:
    doc_id: str
    path: Path
    category: str
    sha256: str
    allowed_roles: tuple[str, ...]


class DocumentEngine:
    def __init__(self) -> None:
        self._index: dict[str, DocumentProof] = {}

    @staticmethod
    def classify(path: Path) -> str:
        name = path.name.lower()
        mapping = {
            "invoice": "invoice",
            "facture": "invoice",
            "quote": "quote",
            "devis": "quote",
            "tax": "tax",
            "proof": "proof",
            "intervention": "intervention",
        }
        for token, category in mapping.items():
            if token in name:
                return category
        return "unknown"

    @staticmethod
    def hash_file(path: Path) -> str:
        content = path.read_bytes()
        return hashlib.sha256(content).hexdigest()

    @staticmethod
    def make_doc_id(path: Path, sha256: str) -> str:
        return f"DOC-{sha256[:12]}-{path.stem[:24]}"

    def index_document(self, path: Path, allowed_roles: tuple[str, ...] = ("admin", "manager")) -> DocumentProof:
        sha256 = self.hash_file(path)
        doc_id = self.make_doc_id(path, sha256)
        proof = DocumentProof(doc_id=doc_id, path=path.resolve(), category=self.classify(path), sha256=sha256, allowed_roles=allowed_roles)
        self._index[doc_id] = proof
        return proof

    def search(self, query: str) -> list[DocumentProof]:
        query_lc = query.lower()
        return [item for item in self._index.values() if query_lc in item.path.name.lower()]

    def delivery_by_doc_id(self, doc_id: str, role: str) -> Path:
        if doc_id not in self._index:
            raise PermissionError("refusal: unknown doc_id")
        item = self._index[doc_id]
        if role not in item.allowed_roles:
            raise PermissionError("refusal: role is not allowed")
        current_hash = self.hash_file(item.path)
        if current_hash != item.sha256:
            raise PermissionError("refusal: file hash changed")
        return item.path

    def require_unambiguous_match(self, query: str) -> DocumentProof:
        matches = self.search(query)
        if len(matches) != 1:
            choices = [f"{i+1}. {doc.path.name}" for i, doc in enumerate(matches)]
            raise ValueError(f"refusal: ambiguous query. choices={choices}")
        return matches[0]
