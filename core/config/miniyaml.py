from __future__ import annotations

from pathlib import Path


def load_simple_yaml(path: str | Path) -> dict:
    lines = Path(path).read_text(encoding="utf-8").splitlines()
    data: dict = {}
    current_key = None
    current_list = None
    current_item = None
    for raw in lines:
        line = raw.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        stripped = line.strip()
        if indent == 0 and stripped.endswith(":"):
            key = stripped[:-1]
            if key == "sources":
                data[key] = []
                current_key = key
            else:
                data[key] = {}
                current_key = key
            current_list = None
            continue
        if current_key == "paths" and indent >= 2 and ":" in stripped:
            k, v = stripped.split(":", 1)
            data["paths"][k.strip()] = v.strip().strip('"')
            continue
        if current_key == "sources":
            if stripped.startswith("-"):
                current_item = {}
                data["sources"].append(current_item)
                rest = stripped[1:].strip()
                if rest:
                    k, v = rest.split(":", 1)
                    current_item[k.strip()] = _coerce(v.strip())
                continue
            if current_item is not None and ":" in stripped:
                k, v = stripped.split(":", 1)
                current_item[k.strip()] = _coerce(v.strip())
                continue
    return data


def _coerce(value: str):
    value = value.strip().strip('"')
    if value in {"true", "false"}:
        return value == "true"
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [chunk.strip() for chunk in inner.split(",")]
    return value
