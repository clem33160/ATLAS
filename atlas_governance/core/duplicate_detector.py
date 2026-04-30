from collections import defaultdict
from pathlib import Path

from .common import iter_project_files, repo_root, sha256_file, write_json, write_md, runtime_dir

NOISE_DIR_MARKERS = {
    "examples",
    "fixtures",
    "__pycache__",
    ".git",
    "runtime",
}
NOISE_FILE_SUFFIXES = (".example.json", ".example.csv", ".example.md", ".example.html")


def _is_duplicate_relevant(path: Path) -> bool:
    rel_parts = {part.lower() for part in path.parts}
    if rel_parts & NOISE_DIR_MARKERS:
        return False
    name = path.name.lower()
    if name == "__init__.py" or name.endswith(NOISE_FILE_SUFFIXES):
        return False
    # Ignore trivial placeholders that create artificial duplicate groups.
    if path.stat().st_size < 32:
        return False
    return True


def run_duplicate_detection():
    root = repo_root()
    by = defaultdict(list)
    skipped_noise = 0

    for p in iter_project_files(include_runtime=False):
        rel = p.relative_to(root)
        if not _is_duplicate_relevant(rel):
            skipped_noise += 1
            continue
        by[sha256_file(p)].append(str(rel))

    groups = [g for g in by.values() if len(g) > 1]
    out = {
        "count": len(groups),
        "duplicate_groups": groups,
        "skipped_noise_files": skipped_noise,
        "policy": "ignore fixtures/examples/runtime/__init__/tiny placeholders",
    }
    write_json(runtime_dir() / "reports/duplicates.json", out)
    write_md(
        runtime_dir() / "reports/duplicates.md",
        "# Duplicates\n"
        f"- skipped_noise_files: {skipped_noise}\n"
        f"- policy: {out['policy']}\n\n"
        + "\n".join([", ".join(g) for g in groups]),
    )
    return out
