from __future__ import annotations


def read_ranges(api_read_fn, spreadsheet_id: str, ranges: list[str]) -> dict[str, list[list[str]]]:
    return api_read_fn(spreadsheet_id, ranges)


def map_rows(domain: str, rows: list[list[str]]) -> list[dict]:
    headers = rows[0] if rows else []
    return [dict(zip(headers, r)) for r in rows[1:]]
