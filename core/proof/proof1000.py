from __future__ import annotations

from pathlib import Path
from dataclasses import dataclass

from core.documents.engine import DocumentEngine


@dataclass
class Proof1000Result:
    PASS: int
    WARN: int
    FAIL: int
    CRITICAL_FAIL: int


def run_proof1000(sandbox_root: Path) -> Proof1000Result:
    sandbox_root.mkdir(parents=True, exist_ok=True)
    engine = DocumentEngine()
    categories = ["invoice", "quote", "proof", "tax", "intervention"]
    docs: list[str] = []
    for i in range(1000):
        category = categories[i % len(categories)]
        p = sandbox_root / f"{category}_{i:04d}.txt"
        p.write_text(f"fake {category} document {i}\n", encoding="utf-8")
        docs.append(str(p))
        engine.index_document(p)

    pass_count = 0
    warn_count = 0
    fail_count = 0
    critical_fail = 0

    if len(docs) == 1000:
        pass_count += 1
    else:
        critical_fail += 1

    all_exist = all(Path(doc).exists() for doc in docs)
    pass_count += int(all_exist)
    critical_fail += int(not all_exist)

    hash_ok = True
    for proof in list(engine._index.values()):
        if engine.hash_file(proof.path) != proof.sha256:
            hash_ok = False
            break
    pass_count += int(hash_ok)
    critical_fail += int(not hash_ok)

    try:
        engine.require_unambiguous_match("invoice")
        fail_count += 1
    except ValueError:
        pass_count += 1

    one_doc = next(iter(engine._index.values()))
    try:
        engine.delivery_by_doc_id(one_doc.doc_id, "admin")
        pass_count += 1
    except Exception:
        fail_count += 1

    try:
        engine.delivery_by_doc_id(one_doc.doc_id, "apprentice")
        fail_count += 1
    except PermissionError:
        pass_count += 1

    one_doc.path.write_text("tampered", encoding="utf-8")
    try:
        engine.delivery_by_doc_id(one_doc.doc_id, "admin")
        fail_count += 1
    except PermissionError:
        pass_count += 1

    return Proof1000Result(PASS=pass_count, WARN=warn_count, FAIL=fail_count, CRITICAL_FAIL=critical_fail)
